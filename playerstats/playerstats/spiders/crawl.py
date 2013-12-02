import json

from scrapy.selector import Selector, HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http.request import Request
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

from playerstats.items import GameItem

# PlayerStatsSpider
# Author: lpa22
#
# This spider scrapes pro-football-reference.com for data regarding player stats

# Player table initialization
player_dictionary = {}

class CrawlSpider(CrawlSpider):
    name = 'crawl'
    allowed_domains = ['pro-football-reference.com']

    # The range of years (these can later be added as parameters)
    min_year = 1998
    max_year = 2013

    # Initialize the starting urls
    start_urls = []

    # Develop the start urls based on the years
    start_urls = []
    for i in range(min_year, max_year):
        start_urls.append(
            'http://www.pro-football-reference.com/years/' + str(i) + '/games.htm'
        )

    def __init__(self):
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def parse(self, response):
        # Grab and traverse to all links to boxscores
        link_sel = Selector(response)
        links = link_sel.xpath('//table[@id="games"]//a[contains(text(),"boxscore")]/@href').extract()

        for link in links:
            cleaned_url = "http://www.pro-football-reference.com" + link
            yield Request(cleaned_url, callback=self.parse_page)

    def parse_page(self, response):
      sel = Selector(response)
      game_time = sel.xpath('//table[1]/tr/td[1]/node()').extract()

      if str(game_time[0]).split(' ')[0].lower() == 'week':
          week = int(game_time[0].split(' ')[1])
          year = int(game_time[2])

          player_table = sel.xpath('//table[@id="skill_stats"]/tbody/tr')

          for player in player_table:
            name = player.xpath('td[1]/a/text()').extract()
            if name != []:
                player_name = str(name[0])

                if player_name not in player_dictionary:
                    player_dictionary[player_name] = {}

                if year not in player_dictionary[player_name]:
                    player_dictionary[player_name][year] = {}

                player_dictionary[player_name][year][week] = self.generate_player_game(player)

    def generate_player_game(self,player):
        stats = []

        for x in [3,4,5,6,7,9,10,11,13,14,15]:
            raw_stat = player.xpath('td['+str(x)+']/text()').extract()
            clean_stat = 0 if raw_stat == [] else int(raw_stat[0])
            stats.append(clean_stat)

        return stats

    def spider_closed(self):
        players = open('players.json','w')
        players.write(json.dumps(player_dictionary, sort_keys=True,separators=(',',':')))
        players.close()

      




