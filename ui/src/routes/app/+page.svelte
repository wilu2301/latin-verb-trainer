<script xmlns="http://www.w3.org/1999/html">
	import axios from 'axios';

	const API_URL = 'http://localhost:8000';

	let error = false;
	let verb = {
		infinitive: '',
		praesens: '',
		perfekt: '',
		ppp: '',
		translation: [],
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

	let textfield = '';

	let hint_level = 0;

	function throwError(caller = 'Unknown', message = 'Unknown error') {
		error = true;
		console.log(
			'%c' + 'Errare humanum est.',
			'color: #7289DA; -webkit-text-stroke: 2px black; font-size: 72px; font-weight: bold;'
		);
		console.error('[Error] ' + caller + ': ' + message);
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
			.get(API_URL + '/verb/?infinitive=' + verb, {
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
		verb.translation = verb_json.translations;
		verb.konjugation = verb_json.konjugation;
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
		} catch (e) {
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

		console.log(correct);
	}

	function transform_goal() {
		instruction = '';

		// Persona
		if (form.persona < 4) {
			instruction += form.persona + '. Person Singular ';
		} else {
			instruction += form.persona - 3 + '. Person Plural ';
		}

		// Tempus
		if (form.tempus === 'praesens') {
			instruction += 'Präsens';
		} else if (form.tempus === 'imperfekt') {
			instruction += 'Imperfekt';
		} else if (form.tempus === 'perfekt') {
			instruction += 'Perfekt';
		} else if (form.tempus === 'plusquamperfekt') {
			instruction += 'Plusquamperfekt';
		} else if (form.tempus === 'futur1') {
			instruction += 'Futur 1';
		} else if (form.tempus === 'futur2') {
			instruction += 'Futur 2';
		}

		// Modus
		if (form.modus === 'indicative') {
			instruction += ' Indikativ';
		} else if (form.modus === 'conjunctive') {
			instruction += ' Konjunktiv';
		}

		// Genus Verbi

		if (form.genus_verbi === 'active') {
			instruction += ' Aktiv';
		} else if (form.genus_verbi === 'passive') {
			instruction += ' Passiv';
		}
	}

	function check() {
		if (textfield === correct) {
			alert('Richtig!');
			get_random_verb();
		} else {
			alert('Falsch!');
		}
	}
</script>

<div class="app">
	<div class="settings">
		<img src="icons/info.svg" alt="settings" />
	</div>

	<div class="goal-form">
		<h2>{instruction}</h2>
	</div>

	<div class="verb">
		<div class="inline">
			<h1>
				{verb.infinitive},
			</h1>
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
		</div>
		<p>
			{#if verb.konjugation !== null}
				{verb.konjugation}
			{/if}
		</p>
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
	</div>

	<div class="answer">
		<button id="help">
			<img src="icons/help.svg" alt="help" />
		</button>
		<input type="text" bind:value={textfield} />
		<button id="check" on:click={check}>
			<img src="icons/check.svg" alt="check" />
		</button>
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

	.settings {
		position: fixed;
		top: 0;
		right: 0;
		padding: 1rem;

		img {
			width: 2.2rem;
			height: 2.2rem;
			cursor: pointer;
			transition: 0.1s;
			&:hover {
				transform: scale(1.1);
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

			transition: 0.1s;
			&:hover {
				background-color: #6320ee;
				scale: 1.1;
			}
		}
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
