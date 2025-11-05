import { writeFile, readFile } from 'node:fs/promises';
import type { ExperimentResult } from '$lib/types';

const RESULTS_FILE = 'experiment-results.json';

export const actions = {
	saveResult: async ({ request }: { request: Request }) => {
		const data = await request.formData();
		const resultJson = data.get('result');
		
		if (!resultJson) {
			return { success: false, error: 'No result data' };
		}

		try {
			const result: ExperimentResult = JSON.parse(resultJson as string);
			
			// Read existing results
			let results: ExperimentResult[] = [];
			try {
				const existingData = await readFile(RESULTS_FILE, 'utf-8');
				results = JSON.parse(existingData);
			} catch (err) {
				// File doesn't exist yet, start with empty array
				results = [];
			}

			// Add new result
			results.push(result);

			// Write back to file
			await writeFile(RESULTS_FILE, JSON.stringify(results, null, 2), 'utf-8');

			return { success: true };
		} catch (error) {
			console.error('Error saving result:', error);
			return { success: false, error: 'Failed to save result' };
		}
	}
};
