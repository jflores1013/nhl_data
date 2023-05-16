import requests
import pandas as pd

# Set the base URL for the NHL API
base_url = "https://statsapi.web.nhl.com/api/v1"

# Set the endpoint for the teams
teams_endpoint = "/teams"

# Send a GET request to the NHL API
response = requests.get(base_url + teams_endpoint)

# Parse the response as a dictionary
response_dict = response.json()

# Create an empty list to store the team ids
team_id_list = []

# Iterate over the teams in the response
for team in response_dict['teams']:
    # Extract the team id
    team_id = team['id']

    # Append the team id to the team_id_list
    team_id_list.append(team_id)

# Create a set of the team ids
team_id_set = set(team_id_list)

# Convert the set to a list
team_id_list = list(team_id_set)

# Create a Pandas dataframe
df = pd.DataFrame()

# Iterate over the team ids in the team_id_list
for team_id in team_id_list:
    # Set the base URL for the NHL API
    base_url = "https://statsapi.web.nhl.com/api/v1"

    # Set the endpoint for the specific team
    team_endpoint = f"/teams/{team_id}?expand=team.roster"

    # Send a GET request to the NHL API
    response = requests.get(base_url + team_endpoint)

    # Parse the response as a dictionary
    response_dict = response.json()

    # Access the roster data
    roster = response_dict["teams"][0]["roster"]["roster"]

    # Create a Pandas dataframe from the roster data
    df = df.append(roster)

# Use the json_normalize() method to extract each element in the person column into separate columns
person_df = pd.json_normalize(df['person'])

# Create an empty list to store the game log data for each player
game_logs = []

# Iterate over the rows in person_df
for index, row in person_df.iterrows():
  # Get the player's id
  player_id = row['id']
  
  # Set the endpoint for the player's game log
  endpoint = f"/people/{player_id}/stats?stats=gameLog"
  
  # Send a GET request to the NHL API
  response = requests.get(base_url + endpoint)
  
  # Parse the response as a dictionary
  response_dict = response.json()
  
  # Get the game log data from the response
  game_log = response_dict['stats'][0]['splits']

  # Add the player's id to each game log entry
  for entry in game_log:
    entry['player_id'] = player_id
  
  # Add the game log data to the list
  game_logs.extend(game_log)

# Create a dataframe from the list of game logs
game_log_df = pd.json_normalize(game_logs)

print(game_log_df)

game_log_df.to_csv('C:/Users/jared\Projects/nhl_data/nhl_game_log.csv')
