# NHL Play-by-Play Data Extraction

This Python script fetches game data from the NHL API, processes it, and exports it into a CSV file. The output file, `nhl_play_by_play_data_all_games.csv`, is suitable for further analysis or visualization in a tool like Tableau. The script is easy to run and customizable based on the dates you're interested in.

## Features

- Fetches data about NHL teams and their games.
- Extracts play-by-play data for each game.
- Extracts player-specific data nested within each play.
- Processes and cleans the data for further analysis.
- Exports the data to a CSV file.

## Requirements

- Python 3.6 or later
- `requests` library for making HTTP requests
- `pandas` library for data manipulation and analysis
- `datetime` for date manipulations

## How to Run

1. Install the necessary Python packages if you haven't already:

   ```
   pip install requests pandas
   ```

2. Run the Python script:

   ```
   python nhl_data.py
   ```

3. The script will fetch the data and create a CSV file called `nhl_play_by_play_data_all_games.csv` in the same directory.

## Customization

You can customize the date range for which the script fetches game data. To do this, modify the `startDate` and `endDate` values in the following line of code:

```python
team_endpoint = f"/schedule?startDate=2022-10-07&endDate={yesterday}&teamId={team_id}"
```

Replace `2022-10-07` with your desired start date and `{yesterday}` with your desired end date. Make sure to keep the date format as `YYYY-MM-DD`.

## Limitations

Please note that the script fetches a large amount of data, which might make it run slowly depending on your internet speed and the date range you've specified. Also, while the NHL API is currently free to use without an API key, this might change in the future.

## Support

If you have any questions or run into any issues, feel free to reach out. I'll be happy to help!

## Future Improvements

- Add error handling for API requests.
- Implement data caching to improve performance for repeated runs.
- Add command line arguments for specifying the date range.
