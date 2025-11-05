import type { Table, BookingSlot, Prompt, ExperimentData } from './types';

// Generate random table layout (minimum 4 of each capacity)
function generateTables(): Table[] {
	const numFourPerson = 4 + Math.floor(Math.random() * 5); // 4-8 tables for 4 people
	const numSixPerson = 12 - numFourPerson; // Remaining are for 6 people (4-8)
	
	const tables: Table[] = [];
	let id = 1;
	
	// Add 4-person tables with random shapes (can be circle OR square)
	for (let i = 0; i < numFourPerson; i++) {
		const shape: 'circle' | 'square' = Math.random() > 0.5 ? 'circle' : 'square';
		tables.push({ id: id++, shape, capacity: 4 });
	}
	
	// Add 6-person tables with random shapes (can be circle OR square)
	for (let i = 0; i < numSixPerson; i++) {
		const shape: 'circle' | 'square' = Math.random() > 0.5 ? 'circle' : 'square';
		tables.push({ id: id++, shape, capacity: 6 });
	}
	
	// Shuffle the tables array to randomize their order/position
	for (let i = tables.length - 1; i > 0; i--) {
		const j = Math.floor(Math.random() * (i + 1));
		[tables[i], tables[j]] = [tables[j], tables[i]];
	}
	
	return tables;
}

// Restaurant has 12 tables with random distribution
const TABLES: Table[] = generateTables();

const AVAILABLE_TIMES = [
	'17:00', '17:30', '18:00', '18:30', '19:00', '19:30', '20:00', '20:30', '21:00'
];

function formatTimeForDisplay(time24: string): string {
	const [hours, minutes] = time24.split(':').map(Number);
	const period = hours >= 12 ? 'PM' : 'AM';
	const displayHour = hours > 12 ? hours - 12 : hours === 0 ? 12 : hours;
	return minutes === 0 ? `${displayHour}${period}` : `${displayHour}:${minutes}${period}`;
}

function generateRandomPrompt(): Prompt {
	const partySizes = [4, 6];
	const partySize = partySizes[Math.floor(Math.random() * partySizes.length)];
	const time = AVAILABLE_TIMES[Math.floor(Math.random() * AVAILABLE_TIMES.length)];
	
	return {
		partySize,
		time,
		displayTime: formatTimeForDisplay(time)
	};
}

function addMinutes(time: string, minutes: number): string {
	const [hours, mins] = time.split(':').map(Number);
	const totalMinutes = hours * 60 + mins + minutes;
	const newHours = Math.floor(totalMinutes / 60) % 24;
	const newMins = totalMinutes % 60;
	return `${String(newHours).padStart(2, '0')}:${String(newMins).padStart(2, '0')}`;
}

function timeToMinutes(time: string): number {
	const [hours, mins] = time.split(':').map(Number);
	return hours * 60 + mins;
}

function timesOverlap(start1: string, end1: string, start2: string, end2: string): boolean {
	const s1 = timeToMinutes(start1);
	const e1 = timeToMinutes(end1);
	const s2 = timeToMinutes(start2);
	const e2 = timeToMinutes(end2);
	
	return s1 < e2 && s2 < e1;
}

export function generateExperimentData(systemType: 'coloured' | 'text'): ExperimentData {
	// Generate new random table layout for each trial
	const tables = generateTables();
	
	const prompt = generateRandomPrompt();
	const bookings: BookingSlot[] = [];
	
	// Find tables that can accommodate the party size
	const suitableTables = tables.filter(table => {
		// Party of 4 needs circle table (capacity 4)
		// Party of 6 needs square table (capacity 6)
		return table.capacity === prompt.partySize;
	});
	
	// Ensure at least one suitable table is available at the requested time
	const guaranteedAvailableTable = suitableTables[Math.floor(Math.random() * suitableTables.length)];
	
	// Generate random bookings for all tables
	tables.forEach(table => {
		// For each table, randomly pick a few time slots to book (not all of them)
		// This creates a more realistic booking pattern
		const numBookings = Math.floor(Math.random() * 4); // 0-3 bookings per table
		const availableSlots = [...AVAILABLE_TIMES];
		
		for (let i = 0; i < numBookings && availableSlots.length > 0; i++) {
			const randomIndex = Math.floor(Math.random() * availableSlots.length);
			const time = availableSlots[randomIndex];
			availableSlots.splice(randomIndex, 1); // Remove this slot so we don't book it twice
			
			// Special handling for the guaranteed table
			if (table.id === guaranteedAvailableTable.id) {
				// Check if this booking would conflict with the prompt time
				const bookingEnd = addMinutes(time, 90);
				const promptEnd = addMinutes(prompt.time, 90);
				
				// Only add booking if it doesn't overlap with prompt time
				if (!timesOverlap(time, bookingEnd, prompt.time, promptEnd)) {
					bookings.push({
						tableId: table.id,
						startTime: time,
						endTime: bookingEnd
					});
				}
			} else {
				// For other tables, add the booking normally
				bookings.push({
					tableId: table.id,
					startTime: time,
					endTime: addMinutes(time, 90)
				});
			}
		}
	});
	
	return {
		systemType,
		bookings,
		tables, // Use the newly generated tables for this trial
		prompt
	};
}

export function isTableAvailable(
	tableId: number,
	selectedTime: string,
	bookings: BookingSlot[]
): boolean {
	const endTime = addMinutes(selectedTime, 90);
	
	return !bookings.some(booking => 
		booking.tableId === tableId &&
		timesOverlap(selectedTime, endTime, booking.startTime, booking.endTime)
	);
}

export { AVAILABLE_TIMES, TABLES };
