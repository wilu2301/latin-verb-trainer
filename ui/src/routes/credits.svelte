<script>
	import translations from '../translations.js';
	import { dict, t } from '../i18n.js';

	$: dict.set(translations);

	export let credits;

	let fadeOut = false;
</script>

<div
	class="credits"
	style="opacity: {fadeOut ? 0 : 1}; transform: translateY({fadeOut
		? '20px'
		: '0'}); transition: opacity 0.5s ease, transform 0.5s ease;"
>
	<button
		class="close"
		on:click={() => {
			fadeOut = true;
			setTimeout(() => {
				credits = false;
			}, 500);
		}}
	>
		{$t('credits.close')}
	</button>

	<h1>{$t('credits.title')}</h1>
	<p>
		{$t('credits.text')}
	</p>
	<h2>{$t('credits.help')}</h2>
	<table>
		<thead>
			<tr>
				<th>{$t('credits.table.head.amount')}</th>
				<th>{$t('credits.table.head.action')}</th>
				<th>{$t('credits.table.head.flame')}</th>
			</tr>
		</thead>
		<tbody>
			<tr>
				<td>{$t('credits.table.body.1.amount')}</td>
				<td>{$t('credits.table.body.1.action')}</td>
				<td>{$t('credits.table.body.1.flame')}</td>
			</tr>
			<tr>
				<td>{$t('credits.table.body.2.amount')}</td>
				<td>{$t('credits.table.body.2.action')}</td>
				<td>{$t('credits.table.body.2.flame')}</td>
			</tr>
			<tr>
				<td>{$t('credits.table.body.3.amount')}</td>
				<td>{$t('credits.table.body.3.action')}</td>
				<td>{$t('credits.table.body.3.flame')}</td>
			</tr>
		</tbody>
	</table>

	<h2>{$t('credits.footer')}</h2>

	<footer class="footer">
		<p>Made with</p>
		<img src="/icons/heart.svg" alt="heart icon" class="heart-icon" /> by
		<a href="https://wilu.itch.io" target="_blank">wilu</a>
	</footer>
</div>

<style lang="scss">
	a,
	button {
		color: #8075ffff;
		text-decoration: none;
		font-weight: bold;
		transition: color 0.3s ease;
	}

	a:hover,
	button:hover {
		color: #6320eeff;
	}

	button {
		background: none;
		border: none;
		cursor: pointer;
	}

	.credits {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: space-between;
		height: 80%;
		max-width: 700px;
		padding: 20px;
		background-color: #ffffff;
		border-radius: 20px;
		box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
		animation: fadeIn 0.8s ease-in-out;
		overflow: auto;
	}

	.credits h1 {
		color: #6320eeff;
		font-size: 2rem;
		margin: 20px 0;
	}

	.credits p {
		color: #333;
		font-size: 1rem;
		text-align: center;
		line-height: 1.6;
	}

	table {
		font-family: 'Arial', sans-serif;
		border-collapse: collapse;
		width: 100%;
		margin-top: 20px;
		box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
	}

	th,
	td {
		border: 1px solid #dddddd;
		text-align: left;
		padding: 10px;
	}

	th {
		background-color: #6320eeff;
		color: white;
		font-weight: bold;
	}

	tr:nth-child(even) {
		background-color: #f9f9f9;
	}

	tr:nth-child(odd) {
		background-color: #ffffff;
	}

	.footer {
		display: flex;
		align-items: center;
		gap: 5px;
		margin-top: 20px;
	}

	.footer p {
		margin: 0;
		color: #333;
		font-size: 1rem;
	}

	.heart-icon {
		width: 16px;
		height: 16px;
		animation: pulse 1.5s infinite;
	}

	@keyframes pulse {
		0%,
		100% {
			transform: scale(1);
		}
		50% {
			transform: scale(1.2);
		}
	}

	@keyframes fadeIn {
		from {
			opacity: 0;
			transform: translateY(20px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}
</style>
