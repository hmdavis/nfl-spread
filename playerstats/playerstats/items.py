# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class GameItem(Item):
    team = Field()
    # passing
    pass_completions = Field()
    pass_attempts = Field()
    pass_yards = Field()
    pass_TDs = Field()
    pass_INTs = Field()
    #rushing
    rush_attempts = Field()
    rush_yards = Field()
    rush_TDs = Field()
    #receiving
    receiving_rec = Field()
    receiving_yards = Field()
    receiving_TDs = Field()
