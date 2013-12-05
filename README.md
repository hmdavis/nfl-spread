nfl-spread
================

### Collaborators
* Harry Davis
* Tim Lenardo
* Louis Antonelli 
* Shraya Ramani

### Player Dictionary Layout
The player dictionary can be found in players.json and is indexed by player, then by season, then by week. Every season and week that a player was active is present in the dictionary. The value for the week is a size 12 array with values as follows:
* 1) Home/away (bool)
* 2) pass_completions
* 3) pass_attempts
* 4) pass_yards
* 5) pass_TDs
* 6) pass_INTs thrown
* 7) rush_attempts
* 8) rush_yards
* 9) rush_TDs
* 10) receiving_rec
* 11) receiving_yards
* 12) receiving_TDs

Given a roster, number of games, week, year, and home (bool), the roster_stats function in instance_generator.py sums up the stats from the previous given number of games before the given week and season.

### Team Dictionary Layout
The team dictionary can be found in teams.json and is indexed by team, then by season, then by week. Every season and week that a team was active is present in the dictionary. The value for the week is a size 19 array with values as follows:
* 1) Home/away (bool)
* 2) first downs allowed
* 3) rush_attempts against
* 4) rush_yards allowed
* 5) rush_TDs allowed
* 6) pass_completions allowed
* 7) pass_attempts against
* 8) pass_yards allowed
* 9) pass_TDs allowed
* 10) pass_INTs
* 11) sacks
* 12) sacks_yards
* 13) net passing yards (useless)
* 14) total_yards allowed
* 15) fumbles of the other team
* 16) fumbles_recovered
* 17) total_turnovers forced
* 18) penalties of other team
* 19) penalty yards of other team

Given a roster, number of games, week, year, and home (bool), the team_stats function in instance_generator.py sums up the stats from the previous given number of games before the given week and season.

### Game Dictionary Layout
The game dictionary can be found in games.json and is indexed by season, then by week. Every season and week has an array of dictionaries, each dictionary representing a game with the keys as below:
* 'home': home team
* 'away': away yeam
* 'home_roster': home team roster (array of strings)
* 'away_roster': away team roster (array of strings)
* 'margin': home team score - away team score

### Instance Construction
* Home Offensive Features: completion %, pass_yards/completion, pass_TDs, pass_INTs thrown, rush_yards/attempt, rush_TDs, rec_yards/rec, rec_TDs
* Home Defensive Features: completion % allowed, pass_yards/completion allowed, pass_TDs allowed, pass_INTs, rush_yards/attempt allowed, rush_TDs allowed, fumbles recovered, sacks
* Away Offensive Features: (same as home offensive)
* Away Defensive Features: (same as home defensive)

###Graphing
Run `python graph.py` which will show graphs one by one for each of the files on Average Spread and Average Winner with the Training and Testing Accuracy plotted. 




Total of 32 features