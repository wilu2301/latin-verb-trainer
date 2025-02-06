<script>
	import { confetti } from '@tsparticles/confetti';
	import axios from 'axios';
	import { onMount } from 'svelte';

	import translations from '../translations.js';
	import { dict, locale, t } from '../i18n.js';

	$: languages = Object.keys(translations);
	$: dict.set(translations);

	import Credits from './credits.svelte';
	import ErrorMessage from './errorMessage.svelte';

	let devMode = true;
	let API_URL = 'http://localhost:8000/api';

	let credits = false;

	let error = false;
	let verb = {
		infinitive: '',
		praesens: '',
		perfekt: '',
		ppp: '',
		translation: [],
		translation_en: [],
		translation_de: [],
		konjugation: ''
	};

	let form = {
		tempus: '',
		modus: '',
		genus_verbi: '',
		persona: null
	};

	let correct = '';

	let instruction = '';

	let textfeld = '';

	let textfeld_style = {
		color: 'black'
	};

	let hint_level = 0;

	let streak = {
		value: 0,
		lose: -1
	};

	/*
	Streak system:
	- Correct answer: +1
	- Wrong answer: 0
	- Hint: -1
	- Hint solved: 0
	 */

	onMount(() => {
		/* Init API */
		if (!devMode) {
			API_URL = window.location.origin + '/api';
		}

		get_random_verb();
	});

	function throwError(caller = 'Unknown', message = 'Unknown error') {
		error = true;
		console.log(
			'%c' + 'Errare humanum est.',
			'color: #7289DA; -webkit-text-stroke: 2px black; font-size: 72px; font-weight: bold;'
		);
		console.error('[ErrorMessage] ' + caller + ': ' + message);
	}

	function get_random_verb() {
		axios
			.get(API_URL + '/verb/random_infinitive', {
				timeout: 2000
			})
			.then((response) => {
				verb.infinitive = response.data;
				get_verb(verb.infinitive);
			})
			.catch((error) => {
				throwError('get_random_verb', error);
			});
	}

	function get_verb(verb) {
		axios
			.get(API_URL + '/verb?infinitive=' + verb, {
				timeout: 2000
			})
			.then((response) => {
				transform_verb(response.data);
				find_form(response.data);
				transform_goal();
			})
			.catch((error) => {
				throwError('get_verb', error);
			});
	}

	function transform_verb(verb_json) {
		verb.praesens = verb_json.praesens.active.indicative[0];
		verb.perfekt = verb_json.perfekt.active.indicative[0];
		verb.ppp = verb_json.ppp;
		verb.translation_de = verb_json.translations;
		verb.translation_en = verb_json.translations_en;
		verb.konjugation = verb_json.konjugation;

		update_locale();
	}

	function pick_random_form() {
		const tempi = ['praesens', 'imperfekt', 'perfekt', 'plusquamperfekt', 'futur1', 'futur2'];
		const modi = ['indicative', 'conjunctive'];
		const genus_verbi = ['active', 'passive'];
		const personae = [1, 2, 3, 4, 5, 6];

		let random_tempus = tempi[Math.floor(Math.random() * tempi.length)];
		let random_modus = modi[Math.floor(Math.random() * modi.length)];
		let random_genus_verbi = genus_verbi[Math.floor(Math.random() * genus_verbi.length)];
		let random_persona = personae[Math.floor(Math.random() * personae.length)];

		return [random_tempus, random_modus, random_genus_verbi, random_persona];
	}

	function find_form(verb_full) {
		let picked_form = pick_random_form();
		let tempus = picked_form[0];
		let modus = picked_form[1];
		let genus_verbi = picked_form[2];
		let persona = picked_form[3];

		try {
			correct = verb_full[tempus][genus_verbi][modus][persona - 1];
			if (correct == null) {
				find_form(verb_full);
			}
		} catch {
			console.log(
				'Form: ' + form + ' nicht gefunden für ' + verb_full.infinitive,
				'\nsuche neue...'
			);
			find_form(verb_full);
		}

		form.tempus = tempus;
		form.modus = modus;
		form.genus_verbi = genus_verbi;
		form.persona = persona;
	}

	function transform_goal() {
		instruction = '';

		// Persona
		if (form.persona < 4) {
			instruction +=
				$t('instructions.persona.' + form.persona) +
				' ' +
				$t('instructions.nummerus.singular') +
				' ';
		} else {
			instruction +=
				$t('instructions.persona.' + (form.persona - 3)) +
				' ' +
				$t('instructions.nummerus.plural') +
				' ';
		}

		// Tempus
		if (form.tempus === 'praesens') {
			instruction += $t('instructions.tempi.praesens');
		} else if (form.tempus === 'imperfekt') {
			instruction += $t('instructions.tempi.imperfekt');
		} else if (form.tempus === 'perfekt') {
			instruction += $t('instructions.tempi.perfekt');
		} else if (form.tempus === 'plusquamperfekt') {
			instruction += $t('instructions.tempi.plusquamperfekt');
		} else if (form.tempus === 'futur1') {
			instruction += $t('instructions.tempi.futur1');
		} else if (form.tempus === 'futur2') {
			instruction += $t('instructions.tempi.futur2');
		}

		// Modus
		if (form.modus === 'indicative') {
			instruction += ' ' + $t('instructions.modi.indicative');
		} else if (form.modus === 'conjunctive') {
			instruction += ' ' + $t('instructions.modi.conjunctive');
		}

		// Genus Verbi

		if (form.genus_verbi === 'active') {
			instruction += ' ' + $t('instructions.genus_verbi.active');
		} else if (form.genus_verbi === 'passive') {
			instruction += ' ' + $t('instructions.genus_verbi.passive');
		}
	}

	function check() {
		let successful;

		hint_level = 0;
		textfeld_style.color = 'black';

		if (Array.isArray(correct)) {
			successful = correct.includes(textfeld);
		} else {
			successful = textfeld === correct;
		}

		if (successful) {
			if (streak.lose !== -1) {
				streak.value++;
				streak.value -= streak.lose;

				if (streak.value < 0) {
					streak.value = 0;
				}

				let particles = confetti({
					particleCount: 100,
					spread: 70,
					origin: { y: 0.6 }
				});
				setTimeout(() => {
					particles.then((instance) => {
						instance.destroy();
					});
				}, 3000); // Stop confetti after 3 seconds
			}

			get_random_verb();

			// Cleanup
			textfeld = '';
			streak.lose = 0;
		} else {
			streak.value = 0;
			streak.lose = 0;

			textfeld_style.color = 'red';
			setTimeout(() => {
				textfeld_style.color = 'black';
			}, 2000);
		}
	}

	function get_hint() {
		hint_level++;

		if (hint_level === 1) {
			streak.lose = 1;
		}
		if (hint_level === 2) {
			streak.lose = 2;
		}

		if (hint_level >= 3) {
			streak.lose = -1;
			streak.value = 0;

			if (Array.isArray(correct)) {
				textfeld = correct[0];
			} else {
				textfeld = correct;
			}

			textfeld_style.color = 'green';
		}
	}

	function get_conjugation() {
		if ($locale === 'de') {
			return verb.konjugation;
		} else {
			if (verb.konjugation === 'konsonantische Konjugation') {
				return 'consonant conjugation';
			}
			if (verb.konjugation === 'Unregelmäßiges Verb') {
				return 'irregular verb';
			}

			return verb.konjugation.replace('Konjugation', 'conjugation');
		}
	}

	function update_locale() {
		transform_goal();

		if ($locale === 'de') {
			verb.translation = verb.translation_de;
		} else {
			verb.translation = verb.translation_en;
		}
	}
</script>

<div class="app">
	{#if credits}
		<div class="overlay" id="credits">
			<Credits bind:credits />
		</div>
	{/if}

	{#if error}
		<div class="overlay">
			<ErrorMessage />
		</div>
	{/if}

	<div class="language" on:change={update_locale}>
		<select bind:value={$locale}>
			{#each languages as language}
				<option value={language}>{language}</option>
			{/each}
		</select>
	</div>

	<button
		class="credits_icon"
		on:click={() => {
			credits = !credits;
		}}
	>
		<img alt="settings" src="icons/info.svg" />
	</button>

	<div class="goal-form">
		<h2>{instruction}</h2>
	</div>

	<div class="verb">
		<div class="inline">
			<h1>
				{verb.infinitive}
				{#if hint_level >= 1},{/if}
			</h1>
			{#if hint_level >= 1}
				<h2>
					{#if verb.praesens !== null}
						{verb.praesens},
					{/if}
				</h2>
				<h2>
					{#if verb.perfekt !== null}
						{verb.perfekt},
					{/if}
				</h2>
				<h2>
					{#if verb.ppp !== null}
						{verb.ppp} sum
					{/if}
				</h2>
			{/if}
		</div>
		<p>
			{#if verb.konjugation !== null && hint_level >= 2}
				{get_conjugation()}
			{/if}
		</p>
		{#if verb.translation != null}
			<hr />

			<p>
				{#each verb.translation as translation, index}
					{#if index === 0}
						{translation}
					{/if}
					{#if index > 0 && index < 3}
						, {translation}
					{/if}
				{/each}
			</p>
		{/if}
	</div>

	<div class="bottom">
		<div class="streak" id="streak">
			<img src="icons/flame.svg" alt="streak" />
			<h2>
				{streak.value}
				{#if streak.lose > 0}
					<sup id="lose"
						>{#if streak.lose - 1 <= 0}
							+{:else}
							-{/if}
						{streak.lose - 1}</sup
					>
				{/if}
			</h2>
		</div>

		<div class="answer">
			<button id="help" on:click={get_hint}>
				<img src="icons/help.svg" alt="help" />
			</button>
			<input
				type="text"
				bind:value={textfeld}
				style="color: {textfeld_style.color}"
				placeholder={$t('input.placeholder')}
			/>
			<button id="check" on:click={check}>
				<img src="icons/check.svg" alt="check" />
			</button>
		</div>
	</div>
</div>

<style lang="scss">
	.app {
		height: 100vh;
		width: 100vw;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: space-between;

		animation: background 10s infinite alternate;

		font-family: 'Roboto', sans-serif;
		color: #211a1d;

		overflow: hidden;
	}

	.credits_icon {
		position: fixed;
		top: 0;
		right: 0;
		padding: 1rem;

		background: none;
		border: none;

		img {
			width: 2.2rem;
			height: 2.2rem;
			cursor: pointer;
			transition: 0.3s;
			&:hover {
				transform: scale(1.1);
			}
		}
	}

	.language {
		position: fixed;
		top: 0;
		left: 0;
		padding: 1rem;

		select {
			background: #8075ffff;
			color: #f8f0fbff;
			border: none;
			border-radius: 1rem;
			padding: 1rem;
			transition:
				background-color 0.3s ease,
				color 0.3s ease;

			&:focus {
				background-color: #6320eeff;
				color: #ffffff;
			}
		}

		option {
			background: #8075ffff;
			color: #f8f0fbff;
			border-radius: 1rem;
		}

		&:hover {
			select {
				background: #6320eeff;
			}
			option {
				background: #8075ffff;
			}
		}
	}

	.goal-form {
		text-align: center;
		font-size: 1.8rem;
	}

	.verb {
		width: 80%;
		background-color: white;
		padding: 2rem;
		border-radius: 1rem;
		box-shadow: 0 0 1rem rgba(0, 0, 0, 0.1);

		text-align: center;
		font-size: 2rem;

		.inline {
			display: flex;
			gap: 1rem;
			justify-content: center;
			align-items: baseline;
		}
	}

	.bottom {
		width: 100%;
		display: flex;
		flex-flow: column nowrap;
		justify-content: space-between;
		align-items: center;

		.streak {
			display: flex;
			align-items: center;
			gap: 1rem;
			position: relative;

			img {
				width: 3rem;
				height: 3rem;
			}

			h2 {
				font-size: 2rem;

				#lose {
					color: red;
				}
			}
		}

		.answer {
			width: 90%;
			height: 4rem;
			display: flex;

			align-items: center;
			margin: 2rem;

			input {
				width: 90%;
				height: 100%;
				border: none;
				border-radius: 1rem;
				padding: 1rem;
				font-size: 1.5rem;
				text-align: center;

				box-shadow: 0 0 1rem rgba(0, 0, 0, 0.1);
			}

			button {
				padding: 2rem;
				background-color: #8075ff;
				border: none;
				border-radius: 1rem;
				box-shadow: 0 0 1rem rgba(0, 0, 0, 0.1);
				margin: 0 1rem;
				cursor: pointer;

				transition: 0.3s;

				&:hover {
					background-color: #6320ee;
					scale: 1.1;
				}
			}
		}
	}

	.overlay {
		display: flex;
		justify-content: center;
		align-items: center;
		position: fixed;
		top: 0;
		width: 100vw;
		height: 100%;
		background-color: rgba(0, 0, 0, 0.5);
		z-index: 100;
	}

	@keyframes background {
		0% {
			background-color: #f8f0fb;
		}
		50% {
			background-color: #efe0fb;
		}
		100% {
			background-color: #fbe8f0;
		}
	}

	@keyframes pop {
		50% {
			transform: scale(1.2);
		}
	}

	@media screen and (max-width: 1000px) {
		.verb {
			font-size: 1.5rem;
			margin: 1rem;
		}
		.answer {
			input {
				font-size: 1.2rem;
			}
		}
	}

	@media screen and (max-width: 500px) {
		.app {
			justify-content: flex-start;
		}

		.goal-form {
			font-size: 1.5rem;
			bottom: 0;
		}

		.verb {
			font-size: 1rem;
			margin: 1rem;
		}
		.answer {
			button {
				padding: 1rem;
			}

			input {
				font-size: 1rem;
			}
		}
	}

	@media screen and (max-height: 800px) {
		.app {
			justify-content: flex-start;
		}
	}
</style>
