/**
 * Analysis script for restaurant booking experiment results
 * Run this with: node analyze-results.js
 */

const fs = require('fs');

const RESULTS_FILE = 'experiment-results.json';

function analyzeResults() {
	// Read results file
	let results;
	try {
		const data = fs.readFileSync(RESULTS_FILE, 'utf-8');
		results = JSON.parse(data);
	} catch (error) {
		console.error('Error reading results file:', error.message);
		console.log('Make sure experiment-results.json exists and contains valid JSON.');
		return;
	}

	if (!Array.isArray(results) || results.length === 0) {
		console.log('No results found in the file.');
		return;
	}

	console.log('\n=== Restaurant Booking Experiment Results ===\n');
	console.log(`Total participants: ${results.length}\n`);

	// Collect durations by system
	const colouredDurations = [];
	const textDurations = [];
	
	// Collect order effects
	let colouredFirst = 0;
	let textFirst = 0;

	results.forEach((result) => {
		// Track which system was first
		if (result.firstSystem === 'coloured') {
			colouredFirst++;
		} else {
			textFirst++;
		}

		// Collect durations
		if (result.trial1.system === 'coloured') {
			colouredDurations.push(result.trial1.duration);
		} else {
			textDurations.push(result.trial1.duration);
		}

		if (result.trial2.system === 'coloured') {
			colouredDurations.push(result.trial2.duration);
		} else {
			textDurations.push(result.trial2.duration);
		}
	});

	// Calculate statistics
	const colouredAvg = colouredDurations.reduce((a, b) => a + b, 0) / colouredDurations.length;
	const textAvg = textDurations.reduce((a, b) => a + b, 0) / textDurations.length;
	
	const colouredMedian = median(colouredDurations);
	const textMedian = median(textDurations);

	const colouredStd = standardDeviation(colouredDurations);
	const textStd = standardDeviation(textDurations);

	// Display results
	console.log('--- Order Counterbalancing ---');
	console.log(`coloured system shown first: ${colouredFirst} (${((colouredFirst / results.length) * 100).toFixed(1)}%)`);
	console.log(`Text system shown first: ${textFirst} (${((textFirst / results.length) * 100).toFixed(1)}%)`);

	console.log('\n--- coloured System (with colors) ---');
	console.log(`Sample size: ${colouredDurations.length}`);
	console.log(`Mean duration: ${(colouredAvg / 1000).toFixed(2)}s`);
	console.log(`Median duration: ${(colouredMedian / 1000).toFixed(2)}s`);
	console.log(`Std deviation: ${(colouredStd / 1000).toFixed(2)}s`);
	console.log(`Min: ${(Math.min(...colouredDurations) / 1000).toFixed(2)}s`);
	console.log(`Max: ${(Math.max(...colouredDurations) / 1000).toFixed(2)}s`);

	console.log('\n--- Text System (with labels) ---');
	console.log(`Sample size: ${textDurations.length}`);
	console.log(`Mean duration: ${(textAvg / 1000).toFixed(2)}s`);
	console.log(`Median duration: ${(textMedian / 1000).toFixed(2)}s`);
	console.log(`Std deviation: ${(textStd / 1000).toFixed(2)}s`);
	console.log(`Min: ${(Math.min(...textDurations) / 1000).toFixed(2)}s`);
	console.log(`Max: ${(Math.max(...textDurations) / 1000).toFixed(2)}s`);

	console.log('\n--- Comparison ---');
	const difference = textAvg - colouredAvg;
	const percentDiff = ((difference / colouredAvg) * 100).toFixed(1);
	
	if (difference > 0) {
		console.log(`The coloured system was faster by ${(Math.abs(difference) / 1000).toFixed(2)}s on average (${Math.abs(parseFloat(percentDiff))}% faster)`);
	} else {
		console.log(`The text system was faster by ${(Math.abs(difference) / 1000).toFixed(2)}s on average (${Math.abs(parseFloat(percentDiff))}% faster)`);
	}

	// Learning effect analysis
	console.log('\n--- Learning Effect Analysis ---');
	let trial1Avg = 0;
	let trial2Avg = 0;
	results.forEach((result) => {
		trial1Avg += result.trial1.duration;
		trial2Avg += result.trial2.duration;
	});
	trial1Avg /= results.length;
	trial2Avg /= results.length;

	console.log(`Trial 1 average: ${(trial1Avg / 1000).toFixed(2)}s`);
	console.log(`Trial 2 average: ${(trial2Avg / 1000).toFixed(2)}s`);
	
	if (trial1Avg > trial2Avg) {
		const improvement = ((trial1Avg - trial2Avg) / trial1Avg * 100).toFixed(1);
		console.log(`Trial 2 was ${improvement}% faster (possible learning effect)`);
	}

	console.log('\n===========================================\n');

	// Export summary to CSV
	exportToCsv(results);
}

function median(values) {
	const sorted = [...values].sort((a, b) => a - b);
	const mid = Math.floor(sorted.length / 2);
	return sorted.length % 2 === 0
		? (sorted[mid - 1] + sorted[mid]) / 2
		: sorted[mid];
}

function standardDeviation(values) {
	const avg = values.reduce((a, b) => a + b, 0) / values.length;
	const squareDiffs = values.map(value => Math.pow(value - avg, 2));
	const avgSquareDiff = squareDiffs.reduce((a, b) => a + b, 0) / squareDiffs.length;
	return Math.sqrt(avgSquareDiff);
}

function exportToCsv(results) {
	const csvRows = [
		'Participant,FirstSystem,Trial1System,Trial1Prompt,Trial1Duration(s),Trial2System,Trial2Prompt,Trial2Duration(s)'
	];

	results.forEach((result, index) => {
		csvRows.push(
			`${index + 1},${result.firstSystem},${result.trial1.system},"${result.trial1.prompt}",${(result.trial1.duration / 1000).toFixed(2)},${result.trial2.system},"${result.trial2.prompt}",${(result.trial2.duration / 1000).toFixed(2)}`
		);
	});

	const csvContent = csvRows.join('\n');
	fs.writeFileSync('experiment-results.csv', csvContent);
	console.log('✓ Results exported to experiment-results.csv');
}

// Run analysis
analyzeResults();
