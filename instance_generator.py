# lpa22
# Instance generation

import numpy as np
import math
import json
import argparse

MIN_YEAR = 2000
MAX_YEAR = 2013

# Initialize the player and team dictionaries
players_file = open('playerstats/players.json','r')
player_dictionary = json.loads(players_file.readline())

# TODO 
games_file = open('teamstats/teamstats/games.json','r') 
game_dictionary = json.loads(games_file.readline())

teams_file = open('teamstats/teamstats/teams.json','r')
team_dictionary = json.loads(teams_file.readline())

# Given: A roster of player names as a list, number of past games to sum, game week, year, and home (bool)
# Purpose: Goes specified number of games back from the provided week and year to sum the total offensive
# stats for all players on the roster
def roster_stats(roster, games, week, year, home):
	cumulative_stats = np.array([0]*11)

	for player in roster:
		game_count = 0
		curr_year = year if week > 2 else year-1
		curr_week = week-1 if week > 2 else 17

		while game_count < games and curr_year >= 1998:
			try:
				game_played = player_dictionary[player][str(curr_year)][str(curr_week)]
				if game_played[0] == home:
					cumulative_stats = np.add(cumulative_stats,np.array(game_played[1:]))
					game_count += 1
			except:
				#print player,' inactive week ',curr_week,', ',curr_year
				pass

			curr_week = 17 if curr_week == 1 else curr_week-1
			curr_year = curr_year-1 if curr_week == 17 else curr_year

	#return np.divide(cumulative_stats,float(games))
	return cumulative_stats

# Given: A team name, number of past games to sum, game week, year, and home (bool)
# Purpose: Goes specifeid number of games back from the provided week and year to sum the total defensive
# stats from that period
def defense_stats(team, games, week, year, home):
	cumulative_stats = np.array([0]*18)

	game_count = 0
	curr_year = year if week > 2 else year-1
	curr_week = week-1 if week > 2 else 17

	while game_count < games and curr_year >= 1998:
		try:
			game_played = team_dictionary[team][str(curr_year)][str(curr_week)]
			if game_played[0] == home:
				cumulative_stats = np.add(cumulative_stats,np.array(game_played[1:]))
				game_count += 1
		except:
			pass

		curr_week = 17 if curr_week == 1 else curr_week-1
		curr_year = curr_year-1 if curr_week == 17 else curr_year

	#return np.divide(cumulative_stats,float(games))
	return cumulative_stats

# Given: A home team, an away team, a home roster, an away roster, a week, a year, and games to go back in the past
# Purpose: Generate an instance with the raw offensive and defensive statistics
# Construciton: Home pass_yards/completion
def generate_instance(home, away, home_roster, away_roster, week, year, games):
	defensive_home = defense_stats(home, games, week, year, True)
	defensive_away = defense_stats(away, games, week, year, False)
	offensive_home = roster_stats(home_roster, games, week, year, True)
	offensive_away = roster_stats(away_roster, games, week, year, False)

	instance = []

	### Home Offensive Features
	# completion %

	if float(offensive_home[1]) == 0.0:
		instance.append(0.0)
	else:
		instance.append(float(offensive_home[0])/offensive_home[1])
	# pass_yards/completion
	if float(offensive_home[0]) == 0.0:
		instance.append(0.0)
	else:
		instance.append(float(offensive_home[2])/offensive_home[0])
	# pass_TDs
	instance.append(float(offensive_home[3]))
	# pass_INTs thrown
	instance.append(float(offensive_home[4]))
	# rush_yards/attempt
	instance.append(float(offensive_home[6])/offensive_home[5])
	# rush_TDs
	instance.append(float(offensive_home[7]))
	# rec_yards/rec
	instance.append(float(offensive_home[9])/offensive_home[8])
	# rec_TDs
	instance.append(float(offensive_home[10]))

	### Home Defensive Features
	# completion % allowed
	if float(defensive_home[5]) == 0.0:
		instance.append(0.0)
	else:
		instance.append(float(defensive_home[4])/defensive_home[5])
	# pass_yards/completion allowed
	if float(defensive_home[4]) == 0.0:
		instance.append(0.0)
	else:
		instance.append(float(defensive_home[6])/defensive_home[4])
	# pass_TDs allowed
	instance.append(float(defensive_home[7]))
	# pass_INTs
	instance.append(float(defensive_home[8]))
	# rush_yards/attempt allowed
	if float(defensive_home[1]) == 0.0:
		instance.append(0.0)
	else:
		instance.append(float(defensive_home[2])/defensive_home[1])
	# rush_TDs allowed
	instance.append(float(defensive_home[3]))
	# fumbles recovered
	instance.append(float(defensive_home[14]))
	# sacks
	instance.append(float(defensive_home[9]))

	### Away Offensive Features
	# completion %
	if float(offensive_away[1]) == 0.0:
		instance.append(0.0)
	else:
		instance.append(float(offensive_away[0])/offensive_away[1])
	# pass_yards/completion
	if float(offensive_away[0]) == 0.0:
		instance.append(0.0)
	else:
		instance.append(float(offensive_away[2])/offensive_away[0])
	# pass_TDs
	instance.append(float(offensive_away[3]))
	# pass_INTs thrown
	instance.append(float(offensive_away[4]))
	# rush_yards/attempt
	instance.append(float(offensive_away[6])/offensive_away[5])
	# rush_TDs
	instance.append(float(offensive_away[7]))
	# rec_yards/rec
	instance.append(float(offensive_away[9])/offensive_away[8])
	# rec_TDs
	instance.append(float(offensive_away[10]))

	### Away Defensive Features
	# completion % allowed
	if float(defensive_away[5]) == 0.0:
		instance.append(0.0)
	else:
		instance.append(float(defensive_away[4])/defensive_away[5])
	# pass_yards/completion allowed
	if float(defensive_away[4]) == 0.0:
		instance.append(0.0)
	else:
		instance.append(float(defensive_away[6])/defensive_away[4])
	# pass_TDs allowed
	instance.append(float(defensive_away[7]))
	# pass_INTs
	instance.append(float(defensive_away[8]))
	# rush_yards/attempt allowed
	if float(defensive_away[1]) == 0.0:
		instance.append(0.0)
	else:
		instance.append(float(defensive_away[2])/defensive_away[1])
	# rush_TDs allowed
	instance.append(float(defensive_away[3]))
	# fumbles recovered
	instance.append(float(defensive_away[14]))
	# sacks
	instance.append(float(defensive_away[9]))

	return instance

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
def generate_instance_all(home, away, home_roster, away_roster, week, year, games):
	defensive_home = defense_stats(home, games, week, year, True)
	defensive_away = defense_stats(away, games, week, year, False)
	offensive_home = roster_stats(home_roster, games, week, year, True)
	offensive_away = roster_stats(away_roster, games, week, year, False)

	return offensive_home.tolist() + offensive_away.tolist() + defensive_home.tolist() + defensive_away.tolist()

# Testing with some stats
#print roster_stats(['Dez Bryant','Tony Romo','Miles Austin','Jason Witten'],2,13,2013,False)
#print defense_stats('SEA',2,13,2013,True)


#######################################################

argparser = argparse.ArgumentParser()
argparser.add_argument("season_start", type=int)
argparser.add_argument("season_end", type=int)
argparser.add_argument("week_start", type=int, default=1)
argparser.add_argument("week_end", type=int, default=18)

args = argparser.parse_args()

'''
Create a file containing instances for each game, using a rolling average of x games 
Params:
	games- the number of games to average stats over  
'''
def build_file(game_dictionary,games):
	instance_file = open('training_s' + str(args.season_start)+ '-' + str(args.season_end) + '_w_' + str(args.week_start) + '-' + str(args.week_end) + '.txt','w')
	for season in range(args.season_start,args.season_end):
		for week in range(args.week_start,args.week_end):
			try:
				for game in game_dictionary[str(season)][str(week)]:
					instance = generate_instance(game['home'],game['away'],game['home_roster'],game['away_roster'],week,season,games)
					instance_file.write(str(instance).replace('[','').replace(']','')+', ')
					instance_file.write(str(game['margin'])+'\n')
			except:
				print 'No games in week ',week,' season ',season

	instance_file.close()

for x in range(6,7):
	build_file(game_dictionary,x)

		
	









