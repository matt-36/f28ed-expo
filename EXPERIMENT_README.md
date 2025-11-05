# Restaurant Booking Experiment

This is a user study application designed to collect metrics on how long it takes users to book a specific table at a restaurant using two different systems:

1. **coloured System**: Tables are displayed with color coding (green = available, red = booked)
2. **Text System**: Tables are displayed with text labels ("Available" or "Booked")

## Features

- **Random Data Generation**: Each experiment run generates random booking data
- **Guaranteed Availability**: The system ensures that there's always at least one suitable table available for the given prompt
- **Timing Measurement**: Precise timing of how long it takes users to complete each task
- **Counterbalancing**: Randomly assigns which system is shown first to avoid order effects
- **Data Collection**: All results are saved to `experiment-results.json` with:
  - Timestamp
  - Which system was shown first
  - Prompts given to the user
  - Duration for each trial
  - System type for each trial

## Running the Experiment

1. Install dependencies (if not already done):
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

3. Open the application in your browser (typically at `http://localhost:5173`)

4. Click "Start Experiment" to begin

5. Complete both trials as instructed

6. Results will be automatically saved to `experiment-results.json` in the project root

## Experiment Flow

1. **Intro Screen**: User clicks "Start Experiment"
2. **Trial 1**: 
   - User is randomly assigned to either the coloured or text system
   - User receives a prompt (e.g., "Book a table for 4 at 6PM")
   - Timer starts
   - User selects a time from the dropdown
   - User clicks an available table matching their party size
   - Duration is recorded
3. **Trial 2**: 
   - User is shown the opposite system
   - User receives a different prompt
   - Process repeats
   - Duration is recorded
4. **Complete**: Results are saved and summary is shown

## Table Layout

The restaurant has 12 tables arranged in a 3x4 grid:
- **Circle tables** (5 total): Capacity of 2 people
- **Square tables** (7 total): Capacity of 4 people

For parties of 6, they can use square tables (seated more tightly).

## Available Time Slots

- 5:00 PM (17:00)
- 5:30 PM (17:30)
- 6:00 PM (18:00)
- 6:30 PM (18:30)
- 7:00 PM (19:00)
- 7:30 PM (19:30)
- 8:00 PM (20:00)
- 8:30 PM (20:30)
- 9:00 PM (21:00)

## Data Structure

Results are saved in JSON format with the following structure:

```json
{
  "timestamp": "2025-11-05T...",
  "firstSystem": "coloured" | "text",
  "trial1": {
    "system": "coloured" | "text",
    "prompt": "Book a table for 4 at 6PM",
    "duration": 5234 // milliseconds
  },
  "trial2": {
    "system": "coloured" | "text",
    "prompt": "Book a table for 2 at 7:30PM",
    "duration": 3456 // milliseconds
  }
}
```

## Technical Details

- Built with SvelteKit 2 and Svelte 5
- Uses Vite for development and building
- TypeScript for type safety
- Server-side actions for data persistence
- Responsive design

## Analyzing Results

After collecting data from multiple participants, you can analyze the `experiment-results.json` file to:
- Compare completion times between coloured and text systems
- Check for order effects (first vs second trial)
- Calculate average times for each system
- Perform statistical analysis on the results
