import random
from typing import List
from pybaseball import batting_stats, pitching_stats
from player import Batter, Pitcher
from team import Team

def get_team_batters(year: int, team: str) -> List[Batter]:
stats = batting_stats(year, team)
batters = []
for index, row in stats.iterrows():
name = row['Name']
avg = row['AVG']
obp = row['OBP']
slg = row['SLG']
batter = Batter(name, avg, obp, slg)
batters.append(batter)
return batters

def get_team_pitchers(year: int, team: str) -> List[Pitcher]:
stats = pitching_stats(year, team)
pitchers = []
for index, row in stats.iterrows():
name = row['Name']
era = row['ERA']
whip = row['WHIP']
pitcher = Pitcher(name, era, whip)
pitchers.append(pitcher)
return pitchers

def create_team(year: int, team: str) -> Team:
batters = get_team_batters(year, team)
pitchers = get_team_pitchers(year, team)
return Team(team, batters, pitchers)

def main():
year = 2021
team_name = input("Enter the team name: ")

team = create_team(year, team_name)
print(f"Team {team.name} created with {len(team.batters)} batters and {len(team.pitchers)} pitchers.")

# You can now use this team data to simulate games.
if name == "main":
main()

