nfl-spread
================

### Collaborators
* Harry Davis
* Tim Lenardo
* Louis Antonelli 
* Shraya Ramani

### Player Dictionary Layout
The player dictionary can be found in players.json and is indexed by player, then by season, then by week. Every season and week that a player was active is present in the dictionary. The value for the week is a size 11 array with values as follows:
1) pass_completions
2) pass_attempts
3) pass_yards
4) pass_TDs
5) pass_INTs
6) rush_attempts
7) rush_yards
8) rush_TDs
9) receiving_rec
10) receiving_yards
11) receiving_TDs

Given a roster, number of games, week, year, and home (bool), the roster_stats function in instance_generator.py sums up the stats from the previous given number of games before the given week and season. Still working on getting home to work.