<script lang="ts">
	import { generateExperimentData, AVAILABLE_TIMES } from '$lib/dataGenerator';
	import { isTableAvailable } from '$lib/dataGenerator';
	import RestaurantGrid from '$lib/components/RestaurantGrid.svelte';
	import TableKey from '$lib/components/TableKey.svelte';
	import type { ExperimentData, ExperimentResult } from '$lib/types';

	// Experiment state
	let experimentPhase = $state<'intro' | 'trial1' | 'trial2' | 'complete'>('intro');
	let firstSystem = $state<'coloured' | 'text' | null>(null);
	let trial1Data = $state<ExperimentData | null>(null);
	let trial2Data = $state<ExperimentData | null>(null);
	let currentData = $state<ExperimentData | null>(null);
	
	// Timing
	let startTime = $state<number>(0);
	let trial1Duration = $state<number>(0);
	let trial2Duration = $state<number>(0);
	
	// UI state
	let selectedTime = $state<string | null>(null);
	let showNextButton = $state<boolean>(false);
	let submitting = $state<boolean>(false);
	let errorMessage = $state<string | null>(null);

	function startExperiment() {
		// Randomly assign first system
		firstSystem = Math.random() > 0.5 ? 'coloured' : 'text';
		
		// Generate data for trial 1
		trial1Data = generateExperimentData(firstSystem);
		currentData = trial1Data;
		
		// Start timer
		startTime = Date.now();
		experimentPhase = 'trial1';
		selectedTime = null;
		showNextButton = false;
	}

	function handleTimeSelect(event: Event) {
		const target = event.target as HTMLSelectElement;
		selectedTime = target.value || null;
	}

	function handleTableSelect(tableId: number) {
		if (!currentData || !selectedTime) return;
		
		// Validate the selection
		const table = currentData.tables.find(t => t.id === tableId);
		if (!table) return;
		
		// Check if table is available at selected time
		const isAvailable = isTableAvailable(tableId, selectedTime, currentData.bookings);
		if (!isAvailable) {
			errorMessage = `❌ Error: That table is not available at the selected time. Please try again.`;
			return;
		}
		
		// Check if table has correct capacity for party size
		if (table.capacity !== currentData.prompt.partySize) {
			errorMessage = `❌ Error: Wrong table size! You need a table for ${currentData.prompt.partySize} people. Please try again.`;
			return;
		}
		
		// Check if selected time matches prompt time
		if (selectedTime !== currentData.prompt.time) {
			errorMessage = `❌ Error: Wrong time! You need to book for ${currentData.prompt.displayTime}. Please try again.`;
			return;
		}
		
		// Selection is correct! Clear any error message
		errorMessage = null;
		
		// Record duration
		const duration = Date.now() - startTime;
		
		if (experimentPhase === 'trial1') {
			trial1Duration = duration;
			showNextButton = true;
		} else if (experimentPhase === 'trial2') {
			trial2Duration = duration;
			// Save results
			saveResults();
		}
	}

	function startTrial2() {
		// Generate data for trial 2 with opposite system
		const secondSystem = firstSystem === 'coloured' ? 'text' : 'coloured';
		trial2Data = generateExperimentData(secondSystem);
		currentData = trial2Data;
		
		// Reset UI state
		selectedTime = null;
		showNextButton = false;
		errorMessage = null;
		
		// Start new timer
		startTime = Date.now();
		experimentPhase = 'trial2';
	}

	async function saveResults() {
		if (!trial1Data || !trial2Data || !firstSystem) return;
		
		submitting = true;
		
		const result: ExperimentResult = {
			timestamp: new Date().toISOString(),
			firstSystem,
			trial1: {
				system: trial1Data.systemType,
				prompt: `Book a table for ${trial1Data.prompt.partySize} at ${trial1Data.prompt.displayTime}`,
				duration: trial1Duration
			},
			trial2: {
				system: trial2Data.systemType,
				prompt: `Book a table for ${trial2Data.prompt.partySize} at ${trial2Data.prompt.displayTime}`,
				duration: trial2Duration
			}
		};

		try {
			const formData = new FormData();
			formData.append('result', JSON.stringify(result));
			
			const response = await fetch('?/saveResult', {
				method: 'POST',
				body: formData
			});

			if (response.ok) {
				experimentPhase = 'complete';
			} else {
				alert('Failed to save results');
			}
		} catch (error) {
			console.error('Error saving results:', error);
			alert('Failed to save results');
		} finally {
			submitting = false;
		}
	}

	function resetExperiment() {
		experimentPhase = 'intro';
		firstSystem = null;
		trial1Data = null;
		trial2Data = null;
		currentData = null;
		selectedTime = null;
		showNextButton = false;
		errorMessage = null;
		trial1Duration = 0;
		trial2Duration = 0;
	}
</script>

<svelte:head>
	<title>Restaurant Booking Experiment</title>
	<meta name="description" content="Restaurant booking user study" />
</svelte:head>

<main>
	{#if experimentPhase === 'intro'}
		<div class="intro">
			<h1>Restaurant Booking Experiment</h1>
			<p>
				You will be asked to book tables at a restaurant using two different systems.
				Your task is to complete each booking as quickly as possible.
			</p>
			<p>
				Click the button below to start. You will be given specific instructions for each task.
			</p>
			<button class="start-btn" onclick={startExperiment}>
				Start Experiment
			</button>
		</div>
	{:else if experimentPhase === 'trial1' || experimentPhase === 'trial2'}
		<div class="experiment">
			<div class="header">
				<h2>Trial {experimentPhase === 'trial1' ? '1' : '2'} of 2</h2>
				{#if currentData}
					<div class="instruction">
						Book a table for {currentData.prompt.partySize} at {currentData.prompt.displayTime}
					</div>
				{/if}
			</div>

			<div class="time-selector">
				<label for="time-select">Select a time:</label>
				<select id="time-select" onchange={handleTimeSelect} value={selectedTime || ''}>
					<option value="">-- Select a time --</option>
					{#each AVAILABLE_TIMES as time}
						{@const [hours, minutes] = time.split(':').map(Number)}
						{@const period = hours >= 12 ? 'PM' : 'AM'}
						{@const displayHour = hours > 12 ? hours - 12 : hours === 0 ? 12 : hours}
						{@const displayTime = minutes === 0 ? `${displayHour}:00 ${period}` : `${displayHour}:${minutes} ${period}`}
						<option value={time}>{displayTime}</option>
					{/each}
				</select>
			</div>

			{#if currentData}
				{#if errorMessage}
					<div class="error-message">
						{errorMessage}
					</div>
				{/if}

				<div class="grid-container">
					<h3>Tables for {selectedTime ? (() => {
						const [hours, minutes] = selectedTime.split(':').map(Number);
						const period = hours >= 12 ? 'PM' : 'AM';
						const displayHour = hours > 12 ? hours - 12 : hours === 0 ? 12 : hours;
						return minutes === 0 ? `${displayHour}:00 ${period}` : `${displayHour}:${minutes} ${period}`;
					})() : '...'}</h3>
					
					<div class="grid-with-key">
						<!-- <TableKey /> -->
						<RestaurantGrid
							tables={currentData.tables}
							bookings={currentData.bookings}
							systemType={currentData.systemType}
							{selectedTime}
							onTableSelect={handleTableSelect}
						/>
					</div>
				</div>
			{/if}

			{#if showNextButton}
				<div class="next-section">
					<p>✓ Table booked successfully!</p>
					<button class="next-btn" onclick={startTrial2}>
						Continue to Trial 2
					</button>
				</div>
			{/if}

			{#if submitting}
				<div class="saving">
					<p>Saving results...</p>
				</div>
			{/if}
		</div>
	{:else if experimentPhase === 'complete'}
		<div class="complete">
			<h1>✓ Experiment Complete</h1>
			<p>Thank you for participating! Your results have been saved.</p>
			<div class="results-summary">
				<h3>Summary:</h3>
				<p><strong>Trial 1 ({trial1Data?.systemType}):</strong> {(trial1Duration / 1000).toFixed(2)}s</p>
				<p><strong>Trial 2 ({trial2Data?.systemType}):</strong> {(trial2Duration / 1000).toFixed(2)}s</p>
			</div>
			<button class="reset-btn" onclick={resetExperiment}>
				Run Another Experiment
			</button>
		</div>
	{/if}
</main>

<style>
	main {
		max-width: 800px;
		/* margin: 0 auto; */
		/* padding: 2rem; */
		/* min-height: 100vh; */
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
	}

	.intro {
		text-align: center;
		max-width: 600px;
	}

	.intro h1 {
		font-size: 2.5rem;
		margin-bottom: 1.5rem;
		color: #1f2937;
	}

	.intro p {
		font-size: 1.125rem;
		margin-bottom: 1rem;
		color: #4b5563;
		line-height: 1.6;
	}

	.start-btn, .next-btn, .reset-btn {
		background-color: #3b82f6;
		color: white;
		font-size: 1.25rem;
		padding: 1rem 2rem;
		border: none;
		border-radius: 8px;
		cursor: pointer;
		margin-top: 2rem;
		transition: background-color 0.2s;
	}

	.start-btn:hover, .next-btn:hover, .reset-btn:hover {
		background-color: #2563eb;
	}

	.experiment {
		width: 100%;
		max-width: 700px;
	}

	.header {
		text-align: center;
		margin-bottom: 2rem;
	}

	.header h2 {
		font-size: 1.5rem;
		color: #1f2937;
		margin-bottom: 1rem;
	}

	.instruction {
		background-color: #fef3c7;
		border: 2px solid #f59e0b;
		padding: 1rem;
		border-radius: 8px;
		font-size: 1.25rem;
		font-weight: 600;
		color: #92400e;
	}

	.time-selector {
		margin-bottom: 2rem;
		text-align: center;
	}

	.time-selector label {
		display: block;
		margin-bottom: 0.5rem;
		font-weight: 600;
		color: #1f2937;
	}

	.time-selector select {
		font-size: 1rem;
		padding: 0.5rem 1rem;
		border: 2px solid #d1d5db;
		border-radius: 6px;
		background-color: white;
		cursor: pointer;
	}

	.grid-container {
		margin-bottom: 2rem;
	}

	.grid-container h3 {
		text-align: center;
		margin-bottom: 1rem;
		color: #1f2937;
		font-size: 1.25rem;
	}

	.next-section {
		text-align: center;
		margin-top: 2rem;
	}

	.next-section p {
		font-size: 1.125rem;
		color: #059669;
		font-weight: 600;
		margin-bottom: 1rem;
	}

	.saving {
		text-align: center;
		margin-top: 2rem;
		font-size: 1.125rem;
		color: #3b82f6;
	}

	.complete {
		text-align: center;
		max-width: 600px;
	}

	.complete h1 {
		font-size: 2.5rem;
		color: #059669;
		margin-bottom: 1.5rem;
	}

	.complete p {
		font-size: 1.125rem;
		color: #4b5563;
		margin-bottom: 1rem;
	}

	.results-summary {
		background-color: #f3f4f6;
		padding: 1.5rem;
		border-radius: 8px;
		margin: 2rem 0;
		text-align: left;
	}

	.results-summary h3 {
		margin-bottom: 1rem;
		color: #1f2937;
	}

	.results-summary p {
		margin: 0.5rem 0;
		font-size: 1rem;
	}

	.error-message {
		background-color: #fee2e2;
		border: 2px solid #ef4444;
		color: #991b1b;
		padding: 1rem;
		border-radius: 8px;
		margin-bottom: 1rem;
		font-weight: 600;
		text-align: center;
		animation: shake 0.5s;
	}

	@keyframes shake {
		0%, 100% { transform: translateX(0); }
		10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
		20%, 40%, 60%, 80% { transform: translateX(5px); }
	}

	.grid-with-key {
		display: flex;
		justify-content: center;
		align-items: flex-start;
		gap: 2rem;
	}
</style>
