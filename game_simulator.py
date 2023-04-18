import random 
import pybaseball
from pybaseball import batting_stats, pitching_stats


#The Team class stores the team's name, lineup (list of Player objects), and the current pitcher (a Pitcher object). 
class Team:
    """
    Represents a baseball team with their lineup and current pitcher.
    
    Attributes:
        name (str): The team's name.
        lineup (list of Player): The team's batting lineup (list of Player objects).
        current_batter_index (int): The index of the current batter in the lineup.
        pitcher (Pitcher): The team's current pitcher (a Pitcher object).
    """
    
    def __init__(self, name, lineup, pitcher):
        self.name = name
        self.lineup = lineup
        self.current_batter_index = 0
        self.pitcher = pitcher

    def get_next_batter(self):
        batter = self.lineup[self.current_batter_index]
        self.current_batter_index = (self.current_batter_index + 1) % len(self.lineup)
        return batter

    def __str__(self):
        return self.name

class Player:
    """
    Represents a baseball player with their basic batting statistics.
    
    Attributes:
        name (str): The player's name.
        batting_avg (float): The player's batting average.
        on_base_pct (float): The player's on-base percentage.
        slugging_pct (float): The player's slugging percentage.
        position (int): The player's position in the lineup (1-9).
    """
    
    def __init__(self, name, batting_avg, on_base_pct, slugging_pct, position):
        self.name = name
        self.batting_avg = batting_avg
        self.on_base_pct = on_base_pct
        self.slugging_pct = slugging_pct
        self.position = position

    def __str__(self):
        return f"{self.name} ({self.position})"

class Pitcher:
    """
    Represents a baseball pitcher with their basic pitching statistics.
    
    Attributes:
        name (str): The pitcher's name.
        era (float): The pitcher's earned run average.
        whip (float): The pitcher's walks plus hits per inning pitched.
        strikeouts_per_nine (float): The pitcher's strikeouts per nine innings.
        walks_per_nine (float): The pitcher's walks per nine innings.
    """
    
    def __init__(self, name, era, whip, strikeouts_per_nine, walks_per_nine):
        self.name = name
        self.era = era
        self.whip = whip
        self.strikeouts_per_nine = strikeouts_per_nine
        self.walks_per_nine = walks_per_nine

    def __str__(self):
        return self.name

class Game:
    def __init__(self, home_team, away_team):
        self.home_team = home_team
        self.away_team = away_team
        self.current_inning = 1
        self.half_inning = "top"  # "top" or "bottom"
        self.home_score = 0
        self.away_score = 0
        self.outs = 0

    def add_runs(self, runs, team):
        if team == self.home_team:
            self.home_score += runs
        else:
            self.away_score += runs

    def record_out(self):
        self.outs += 1
        if self.outs >= 3:
            self.switch_half_inning()

    def switch_half_inning(self):
        if self.half_inning == "top":
            self.half_inning = "bottom"
        else:
            self.half_inning = "top"
            self.current_inning += 1
        self.outs = 0

    def is_game_over(self):
        return self.current_inning > 9 and self.half_inning == "top" and self.home_score != self.away_score

    def get_winner(self):
        if self.home_score > self.away_score:
            return self.home_team
        elif self.away_score > self.home_score:
            return self.away_team
        else:
            return "Tie"

#The simulate_at_bat function takes in the batter, pitcher, and game state as input and returns the
#outcome of the at-bat. In this example, we'll use a simple probability model based on the batter's
#on-base percentage (OBP) to determine the outcome
    def simulate_at_bat(batter, pitcher, game_state):
        """
    Simulates a single at-bat between a batter and a pitcher, returning the outcome as a string.
    
    Args:
        batter (Player): The batter (a Player object).
        pitcher (Pitcher): The pitcher (a Pitcher object).
        game_state (Game): The current game state (a Game object).
    
    Returns:
        str: The outcome of the at-bat ("hit" or "out").
    """
        # A simple probability model based on the batter's on-base percentage (OBP)
        random_num = random.random()
        if random_num <= batter.on_base_pct:
            # Batter reaches base
            return "hit"
        else:
            # Batter is out
            return "out"
#The simulate_half_inning function simulates one half-inning (top or bottom) by repeatedly calling the
#simulate_at_bat function until three outs are recorded.
    def simulate_half_inning(team, opposing_pitcher, game_state):
        """
    Simulates a half-inning for a team, updating the game state with the number of runs scored.
    
    Args:
        team (Team): The batting team (a Team object).
        opposing_pitcher (Pitcher): The opposing team's pitcher (a Pitcher object).
        game_state (Game): The current game state (a Game object).
    """
        outs = 0
        runs = 0

        while outs < 3:
            batter = team.get_next_batter()
            outcome = simulate_at_bat(batter, opposing_pitcher, game_state)

            if outcome == "hit":
                runs += 1
            elif outcome == "out":
                outs += 1

        game_state.add_runs(runs, team)

#The simulate_game function simulates the full game by calling the simulate_half_inning function for each
#half-inning until the game is over.
    def simulate_game(home_team, away_team):
        """
    Simulates a full baseball game between two teams, printing the winner and final score at the end.
    
    Args:
        home_team (Team): The home team (a Team object).
        away_team (Team): The away team (a Team object).
    """
    
        game_state = Game(home_team, away_team)
        
        while not game_state.is_game_over():
            if game_state.half_inning == "top":
                simulate_half_inning(away_team, home_team.pitcher, game_state)
            else:
                simulate_half_inning(home_team, away_team.pitcher, game_state)

        game_state.switch_half_inning()

        winner = game_state.get_winner()
        print(f"The winner is {winner} with a score of {game_state.home_score}-{game_state.away_score}")

#The get_user_input function can be created to gather user input for team names, player names, and statistics.
#You can then use the pybaseball library to fetch the player and pitcher statistics for the given names.

    def get_user_input():
        """
    Gathers user input for team names, player names, and starting pitcher names, creating Team objects.
    
    Returns:
        Tuple[Team, Team]: A tuple containing the home team and away team (both Team objects).
    """
    
        home_team_name = input("Enter the home team name: ")
        away_team_name = input("Enter the away team name: ")

        home_lineup = []
        away_lineup = []

        for i in range(1, 10):
            player_name = input(f"Enter the home team player {i} name: ")
            player_data = get_player_batting_stats(player_name)
            if player_data:
                player = Player(player_data["Name"], player_data["AVG"], player_data["OBP"], player_data["SLG"], i)
                home_lineup.append(player)

        for i in range(1, 10):
            player_name = input(f"Enter the away team player {i} name: ")
            player_data = get_player_batting_stats(player_name)
            if player_data:
                player = Player(player_data["Name"], player_data["AVG"], player_data["OBP"], player_data["SLG"], i)
                away_lineup.append(player)

        home_pitcher_name = input("Enter the home team starting pitcher name: ")
        home_pitcher_data = get_pitcher_stats(home_pitcher_name)

        away_pitcher_name = input("Enter the away team starting pitcher name: ")
        away_pitcher_data = get_pitcher_stats(away_pitcher_name)

        home_pitcher = Pitcher(home_pitcher_data["Name"], home_pitcher_data["ERA"], home_pitcher_data["WHIP"], home_pitcher_data["K/9"], home_pitcher_data["BB/9"])
        away_pitcher = Pitcher(away_pitcher_data["Name"], away_pitcher_data["ERA"], away_pitcher_data["WHIP"], away_pitcher_data["K/9"], away_pitcher_data["BB/9"])

        home_team = Team(home_team_name, home_lineup, home_pitcher)
        away_team = Team(away_team_name, away_lineup, away_pitcher)

        return home_team, away_team

    def get_player_batting_stats(name):
        """
    Fetches a player's batting statistics using the pybaseball library.
    
    Args:
        name (str): The player's name.
    
    Returns:
        dict: A dictionary containing the player's batting statistics, or None if the player is not found.
    """
        stats = batting_stats(2023)  # Replace with the desired year
        player_stats = stats.loc[stats["Name"] == name]
        
        if not player_stats.empty:
            return player_stats.iloc[0].to_dict()
        else:
            print(f"Player {name} not found.")
            return None

    def get_pitcher_stats(name):
        """
    Fetches a pitcher's statistics using the pybaseball library.
    
    Args:
        name (str): The pitcher's name.
    
    Returns:
        dict: A dictionary containing the pitcher's statistics, or None if the pitcher is not found.
    """
        stats = pitching_stats(2023)  # Replace with the desired year
        pitcher_stats = stats.loc[stats["Name"] == name]
        
        if not pitcher_stats.empty:
            return pitcher_stats.iloc[0].to_dict()
        else:
            print(f"Pitcher {name} not found.")
            return None

if __name__ == "__main__":
    home_team, away_team, home_pitcher, away_pitcher = get_user_input()
    simulate_game(home_team, away_team, home_pitcher, away_pitcher)
