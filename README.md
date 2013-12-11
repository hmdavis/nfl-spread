nfl-spread
================
Research for a machine learned approach to beating the Las Vegas spread for NFL games.


## Player Dictionary Layout
The player dictionary can be found in players.json and is indexed by player, then by season, then by week. Every season and week that a player was active is present in the dictionary. The value for the week is a size 12 array with values as follows:
* home/away (bool)
* pass_completions
* pass_attempts
* pass_yards
* pass_TDs
* pass_INTs thrown
* rush_attempts
* rush_yards
* rush_TDs
* receiving_rec
* receiving_yards
* receiving_TDs

Given a roster, number of games, week, year, and home (bool), the `roster_stats` function in `instance_generator.py` sums up the stats from the previous given number of games before the given week and season.

## Team Dictionary Layout
The team dictionary can be found in teams.json and is indexed by team, then by season, then by week. Every season and week that a team was active is present in the dictionary. The value for the week is a size 19 array with values as follows:
* home/away (bool)
* first downs allowed
* rush_attempts against
* rush_yards allowed
* rush_TDs allowed
* pass_completions allowed
* pass_attempts against
* pass_yards allowed
* pass_TDs allowed
* pass_INTs
* sacks
* sacks_yards
* net passing yards (useless)
* total_yards allowed
* fumbles of the other team
* fumbles_recovered
* total_turnovers forced
* penalties of other team
* penalty yards of other team

Given a roster, number of games, week, year, and home (bool), the `team_stats` function in `instance_generator.py` sums up the stats from the previous given number of games before the given week and season.

## Game Dictionary Layout
The game dictionary can be found in games.json and is indexed by season, then by week. Every season and week has an array of dictionaries, each dictionary representing a game with the keys as below:
* 'home': home team
* 'away': away team
* 'home_roster': home team roster (array of strings)
* 'away_roster': away team roster (array of strings)
* 'margin': home team score - away team score

## Instance Features
Each feature is `<home features, away features>` `<spread>`, where the features for a single team are:  
* completion %
* pass_yards/completion
* pass_TDs
* pass_INTs thrown
* rush_yards/attempt
* rush_TDs
* rec_yards/rec
* rec_TDs
* completion % allowed
* pass_yards/completion allowed
* pass_TDs allowed
* pass_INTs
* rush_yards/attempt allowed
* rush_TDs allowed
* fumbles recovered
* sacks

## Evaluating Models:
### Prepare data 
Run `python instance_generator.py <params>` where `params` can be: 

### Run models 
Run `python models.py <params> <filepath>` where `params` can be one of: 
* `--dt` for a decision tree regressor 
* `--knn` for a kNN regressor 
* `--svm` for a SVM regressor
* `--rf` for a random forest regressor 

### Graph results
Run `python graph.py` which will show graphs one by one for each of the files on Average Spread and Average Winner with the Training and Testing Accuracy plotted. 

## Collaborators
* Harry Davis
* Tim Lenardo
* Louis Antonelli 
* Shraya Ramani
