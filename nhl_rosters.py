import requests
import pandas as pd

def get_team_ids():
    base_url = "https://statsapi.web.nhl.com/api/v1"
    teams_endpoint = "/teams"
    response = requests.get(base_url + teams_endpoint)
    response_dict = response.json()
    team_id_list = [team['id'] for team in response_dict['teams']]
    return team_id_list

def get_roster(team_id):
    base_url = "https://statsapi.web.nhl.com/api/v1"
    team_endpoint = f"/teams/{team_id}?expand=team.roster"
    response = requests.get(base_url + team_endpoint)
    response_dict = response.json()
    roster = response_dict["teams"][0]["roster"]["roster"]
    return roster

def add_player_details(row):
    player_id = row["id"]
    endpoint = f"/people/{player_id}"
    response = requests.get(base_url + endpoint)
    response_dict = response.json()
    player_details = response_dict["people"][0]
    for key in player_details.keys():
        if key == "currentTeam":
            for sub_key in player_details[key].keys():
                row[f"{key}.{sub_key}"] = player_details[key][sub_key]
        elif key == "primaryPosition":
            for sub_key in player_details[key].keys():
                row[f"{key}.{sub_key}"] = player_details[key][sub_key]
        else:
            row[key] = player_details[key]
    row["headshot_url"] = f"https://cms.nhl.bamgrid.com/images/headshots/current/168x168/{player_id}@2x.jpg"
    return row

base_url = "https://statsapi.web.nhl.com/api/v1"
team_id_list = get_team_ids()
df_list = []
for team_id in team_id_list:
    roster = get_roster(team_id)
    df = pd.DataFrame(roster)
    df_list.append(df)
df = pd.concat(df_list, ignore_index=True)
df = pd.concat([pd.json_normalize(df[col]) for col in ["person", "jerseyNumber", "position"]], axis=1)
df = df.apply(add_player_details, axis=1)
df.to_csv('nhl_roster.csv', index=False)
