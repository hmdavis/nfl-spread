# lpa22
# Instance generation

import numpy as np
import math
import json

MIN_YEAR = 1998

# Initialize the player and team dictionaries
players_file = open('playerstats/players.json','r')
player_dictionary = json.loads(players_file.readline())

# TODO 
games_file = None 
game_dictionary = None

#teams_file = open('teamstats/teams.json','r')
#team_dictionary = json.loads(teams_file.readline())

# Given: A roster of player names as a list, number of past games to sum, game week, year, and home (bool)
# Purpose: Goes specified number of games back from the provided week and year to sum the total offensive
# stats for all players on the roster
def roster_stats(roster, games, week, year,home):
	cumulative_stats = np.array([0]*11)

	for player in roster:
		game_count = 0
		curr_year = year if week > 2 else year-1
		curr_week = week-1 if week > 2 else 17

		while game_count < games and curr_year >= MIN_YEAR:
			try:
				cumulative_stats = np.add(cumulative_stats,np.array(player_dictionary[player][str(curr_year)][str(curr_week)]))
				game_count += 1
			except:
				print player,' inactive week ',curr_week,', ',curr_year
				pass

			curr_week = 17 if curr_week == 1 else curr_week-1
			curr_year = curr_year-1 if curr_week == 17 else curr_year

	return cumulative_stats

# Given: A team name, number of past games to sum, game week, year, and home (bool)
# Purpose: Goes specifeid number of games back from the provided week and year to sum the total defensive
# stats from that period
def defense_stats(team, games, week, year, home):
	cumulative_stats = np.array([0]*11)

	game_count = 0
	curr_year = year if week > 2 else year-1
	curr_week = week-1 if week > 2 else 17

	while game_count < games and curr_year >= MIN_YEAR:
		try:
			cumulative_stats = np.add(cumulative_stats,np.array(team_dictionary[team][str(curr_year)][str(curr_week)]))
			game_count += 1
		except:
			pass

		curr_week = 17 if curr_week == 1 else curr_week-1
		curr_year = curr_year-1 if curr_week == 17 else curr_year

	return cumulative_stats

# Given: A home team, an away team, a home roster, an away roster, a week, a year, and games to go back in the past
# Purpose: Generate an instance with subtracting the offesensive stats from the defensive
# Construction: 
# 1) home rush yards/attempt - away rush yards allowed/attempt
# 2) home receiving yards/reception - away receiving yards allowed/reception
# 3) home rushing TDs - away rushing TDs allowed
# 4) home receiving TDs - away receiving TDs allowed
# 5) home completion % - away completion % allowed
# 6) home pass yards/attempt - away pass yards/attempt allowed
# ..... etc
def generate_instance(home, away, home_roster, away_roster, week, year, games):
	pass


# Testing with some stats
print roster_stats(['Dez Bryant','Tony Romo','Miles Austin','Jason Witten','Felix Jones'],4,12,2011,False)
#print defense_stats('HOU',4,12,2011)


'''
Create a file containing instances for each game, using a rolling average of x games 
Params:
	games- the number of games to average stats over  
'''
def build_file(games): 
	for game in games_dictionary: 
		pass 
	









