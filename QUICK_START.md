# Quick Start Guide

## Running the Experiment

1. **Start the application:**
   ```bash
   npm run dev
   ```

2. **Open in browser:**
   - Navigate to http://localhost:5173
   - You'll see the intro screen

3. **Complete the experiment:**
   - Click "Start Experiment"
   - Follow the instructions for Trial 1
   - Select a time from the dropdown
   - Click an available table that matches the requirements
   - Click "Continue to Trial 2"
   - Repeat for Trial 2
   - Results are automatically saved

## Analyzing Results

After collecting data from multiple participants:

```bash
node analyze-results.js
```

This will:
- Display statistical summaries in the terminal
- Export results to `experiment-results.csv` for further analysis

## Tips for Running the Study

1. **Participant Instructions:**
   - Ask participants to complete tasks as quickly as possible
   - Emphasize accuracy (booking the correct table size and time)
   - Don't help them or give hints during the experiment

2. **Data Collection:**
   - Run multiple participants (aim for at least 20-30 for statistical significance)
   - Results are automatically appended to `experiment-results.json`
   - The system automatically counterbalances which interface is shown first

3. **Between Participants:**
   - No need to reset anything
   - Each participant's data is appended to the existing results
   - The randomization ensures variety in the experiment conditions

## Understanding the Results

### Key Metrics:
- **Duration**: Time from starting the trial to successfully booking a table
- **System Type**: "coloured" (green/red visual indicators) vs "text" ("Available"/"Booked" labels)
- **Order**: Which system was shown first (to detect learning effects)

### What to Look For:
- Which system has a lower average completion time?
- Is there a learning effect (Trial 2 faster than Trial 1)?
- Is the order counterbalancing working (roughly 50/50 split)?
- What's the variability (standard deviation) in each system?

## Troubleshooting

**Server won't start:**
```bash
npm install  # Reinstall dependencies
npm run dev
```

**Results not saving:**
- Check that the file `experiment-results.json` exists
- Ensure you have write permissions in the project directory
- Check the browser console for errors

**Need to reset/clear results:**
```bash
# Backup existing results first!
cp experiment-results.json experiment-results-backup.json
# Then clear:
echo "[]" > experiment-results.json
```

## Data Export

The `analyze-results.js` script creates a CSV file that can be imported into:
- Microsoft Excel
- Google Sheets
- R or Python for statistical analysis
- SPSS or other statistical software

## Good Luck with Your Study! 📊
