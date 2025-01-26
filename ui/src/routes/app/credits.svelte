<script>
	export let credits;

	let fadeOut = false;
</script>

<div
	class="credits"
	style="opacity: {fadeOut ? 0 : 1}; transform: translateY({fadeOut
		? '20px'
		: '0'}); transition: opacity 0.5s ease, transform 0.5s ease;"
>
	<div
		class="close"
		on:click={() => {
			fadeOut = true;
			setTimeout(() => {
				credits = false;
			}, 500);
		}}

	>
		<a>Zurück</a>
	</div>

	<h1>Bilde Lateinische Verbformen!</h1>
	<p>
		Salve, hier kannst du deine Lateinkenntnisse unter Beweis stellen!
		<br />
		Bilde so viele Verbformen wie möglich und erhöhe deine Flamme.
		<br /><br />
		Für jede korrekt gebildete Verbform erhältst du 1 Flamme.
		<br />
		Aber aufgepasst! Für jede falsch gebildete Verbform verlierst du deine Flammen.
	</p>
	<h2>Du brauchst Hilfe?</h2>
	<p>
		Kein Problem! Klicke auf den Button "Hilfe" und erhalte Tipps zur Bildung der Verbformen. <b
			>Aber Achtung:</b
		>
	</p>
	<table>
		<thead>
			<tr>
				<th>Anzahl Hilfe</th>
				<th>Aktion</th>
				<th>Flamme</th>
			</tr>
		</thead>
		<tbody>
			<tr>
				<td>1x</td>
				<td>Zeigt die Stammformen</td>
				<td>Keine Flamme beim Lösen</td>
			</tr>
			<tr>
				<td>2x</td>
				<td>Zeigt die Konjugation</td>
				<td>Verliert eine Flamme beim richtigen Lösen</td>
			</tr>
			<tr>
				<td>3x</td>
				<td>Zeigt die Lösung</td>
				<td>Verliert alle Flammen</td>
			</tr>
		</tbody>
	</table>

	<h2>Worauf wartest du noch?</h2>

	<footer class="footer">
		<p>Made with</p>
		<img src="/icons/heart.svg" alt="heart icon" class="heart-icon" /> by
		<a href="https://wilu.itch.io" target="_blank">wilu</a>
	</footer>
</div>

<style>
	body {
		color: #211a1dff;
		font-family: 'Arial', sans-serif;
		background-color: #f5f5f5;
		display: flex;
		justify-content: center;
		align-items: center;
		height: 100vh;
		margin: 0;
	}

	a {
		color: #8075ffff;
		text-decoration: none;
		font-weight: bold;
		transition: color 0.3s ease;
	}

	a:hover {
		color: #6320eeff;
	}

	.credits {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: space-between;
		height: auto;
		max-width: 700px;
		padding: 20px;
		background-color: #ffffff;
		border-radius: 20px;
		box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
		animation: fadeIn 0.8s ease-in-out;
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
