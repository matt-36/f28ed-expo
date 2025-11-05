export type TableShape = 'circle' | 'square';

export interface Table {
	id: number;
	shape: TableShape;
	capacity: number;
}

export interface BookingSlot {
	tableId: number;
	startTime: string; // Format: "HH:MM"
	endTime: string;   // Format: "HH:MM"
}

export interface Prompt {
	partySize: number;
	time: string; // Format: "HH:MM" (24-hour)
	displayTime: string; // Format for display: "6PM", "7AM", etc.
}

export interface ExperimentData {
	systemType: 'coloured' | 'text';
	bookings: BookingSlot[];
	tables: Table[];
	prompt: Prompt;
}

export interface ExperimentResult {
	timestamp: string;
	firstSystem: 'coloured' | 'text';
	trial1: {
		system: 'coloured' | 'text';
		prompt: string;
		duration: number; // milliseconds
	};
	trial2: {
		system: 'coloured' | 'text';
		prompt: string;
		duration: number; // milliseconds
	};
}
