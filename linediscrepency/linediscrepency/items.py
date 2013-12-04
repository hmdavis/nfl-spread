# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class LinediscrepencyItem(Item):
    #define the fields for your item here like:
    week = Field()
    margin = Field()
    line = Field()
    year = Field()

class Margin(Item):
  margin = Field()
