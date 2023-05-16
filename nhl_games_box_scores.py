import requests
import pandas as pd
import datetime
import os
from datetime import timedelta

# Get yesterday's date
yesterday = datetime.date.today() - timedelta(1)

# Get today's date
today = datetime.date.today()

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

# Create an empty list to store the gamePk values
gamePk_list = []

# Iterate over the team ids in the team_id_list
for team_id in team_id_list:
    # Set the endpoint for the specific team
    team_endpoint = f"/schedule?startDate=2022-10-11&endDate={yesterday}&teamId={team_id}"

    # Send a GET request to the NHL API
    response = requests.get(base_url + team_endpoint)

    # Parse the response as a dictionary
    response_dict = response.json()

    # Iterate over the games in the response
    for game in response_dict['dates']:
        # Extract the gamePk value
        gamePk = game['games'][0]['gamePk']

        # Append the gamePk value to the gamePk_list
        gamePk_list.append(gamePk)

# Create a set of the gamePk values
gamePk_set = set(gamePk_list)

# Convert the set to a list
gamePk_list = list(gamePk_set)

# Create an empty dataframe to store the plays data
score_df = pd.DataFrame()

# Iterate over the gamePk values in the gamePk_list
for gamePk in gamePk_list:

    # Set the endpoint for the specific game
    game_endpoint = f"/game/{gamePk}/feed/live"

    # Send a GET request to the NHL API
    response = requests.get(base_url + game_endpoint)

    # Parse the response as a dictionary
    response_dict = response.json()

    gameDate = response_dict['gameData']['datetime']['dateTime']
    
    gameDate = datetime.datetime.strptime(gameDate, '%Y-%m-%dT%H:%M:%SZ') - timedelta(hours=6)

    temp_score_df = pd.json_normalize(response_dict['liveData']['linescore']['teams'])

    temp_score_df['gamePk'] = gamePk

    temp_score_df['date'] = gameDate

    temp_score_df = temp_score_df.drop(columns=['home.goaliePulled','home.numSkaters','home.powerPlay','away.goaliePulled','away.numSkaters','away.powerPlay'])

    #temp_score_df 
    score_df = score_df.append(temp_score_df)

score_df.to_csv('nhl_games_box_score.csv', index=False)