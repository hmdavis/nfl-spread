# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class TeamstatsItem(Item):
    team_name = Field()
    game = Field()
    '''first_downs = Field()
    rush_attempts= Field()
    rush_yards = Field()
    rush_TDs = Field()
    completions = Field()
    attempts = Field()
    passing_yards = Field()
    passing_TDs = Field()
    passing_INTs = Field()
    sacks = Field()
    sack_yards = Field()
    fumbles = Field()
    fumbles_yards = Field()
    penalties = Field()
    penatly_yards = Field()'''
