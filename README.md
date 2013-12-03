nfl-spread
================

### Collaborators
* Harry Davis
* Tim Lenardo
* Louis Antonelli 
* Shraya Ramani

### Player Dictionary Layout
The player dictionary can be found in players.json and is indexed by player, then by season, then by week. Every season and week that a player was active is present in the dictionary. The value for the week is a size 11 array with values as follows:
*1) pass_completions
*2) pass_attempts
*3) pass_yards
*4) pass_TDs
*5) pass_INTs thrown
*6) rush_attempts
*7) rush_yards
*8) rush_TDs
*9) receiving_rec
*10) receiving_yards
*11) receiving_TDs

Given a roster, number of games, week, year, and home (bool), the roster_stats function in instance_generator.py sums up the stats from the previous given number of games before the given week and season.

### Team Dictionary Layout
The team dictionary can be found in teams.json and is indexed by team, then by season, then by week. Every season and week that a team was active is present in the dictionary. The value for the week is a size 18 array with values as follows:
*1) first downs allowed
*2) rush_attempts against
*3) rush_yards allowed
*4) rush_TDs allowed
*5) pass_completions allowed
*6) pass_attempts against
*7) pass_yards allowed
*8) pass_TDs allowed
*9) pass_INTs
*10) sacks
*11) sacks_yards
*12) net passing yards (useless)
*13) total_yards allowed
*14) fumbles of the other team
*15) fumbles_recovered
*16) total_turnovers forced
*17) penalties of other team
*18) penalty yards of other team

Given a roster, number of games, week, year, and home (bool), the team_stats function in instance_generator.py sums up the stats from the previous given number of games before the given week and season.