# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class TeamItem(Item):
  seasons = Field()

class SeasonItem(Item):
  games = Field()

class GameItem(Item):
    team_one = Field()
    team_two = Field()
    # team 1
    first_downs_one = Field()
    rush_attempts_one = Field()
    rush_yards_one = Field()
    rush_TDs_one = Field()
    completions_one = Field()
    attempts_one = Field()
    passing_yards_one = Field()
    passing_TDs_one = Field()
    passing_INTs_one = Field()
    sacks_one = Field()
    sack_yards_one = Field()
    net_pass_yards_one = Field()
    net_yards_one = Field()
    fumbles_one = Field()
    fumbles_lost_one = Field()
    turnovers_one = Field()
    penalties_one = Field()
    penalty_yards_one = Field()
    # team 2
    first_downs_two = Field()
    rush_attempts_two = Field()
    rush_yards_two = Field()
    rush_TDs_two = Field()
    completions_two = Field()
    attempts_two = Field()
    passing_yards_two = Field()
    passing_TDs_two = Field()
    passing_INTs_two = Field()
    sacks_two = Field()
    sack_yards_two = Field()
    net_pass_yards_two = Field()
    net_yards_two = Field()
    fumbles_two = Field()
    fumbles_lost_two = Field()
    turnovers_two = Field()
    penalties_two = Field()
    penalty_yards_two = Field()

