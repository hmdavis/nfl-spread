import json
#from scrapy.spider import CrawlSpider
from scrapy.selector import Selector
from scrapy.http.request import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from linediscrepency.items import Margin
from linediscrepency.items import LinediscrepencyItem

from math import ceil

# TeamStatsSpider
# Author: ardot
#
# This spider scrapes pro-football-reference.com for data regarding team stats.
# Currently, it gets and prints all team statistics for every game that occured
# in the NFL between the 'min-year' and 'max-year' values
#

team_dictionary= {}

class TeamStatsSpider(CrawlSpider):

  # Start-up required params
  name = 'linespider'
  allowed_domains = ['pro-football-reference.com']

  # The range of years (these can later be added as parameters)
  min_year = 1998
  max_year = 2014

  # Develop the start urls based on the years
  start_urls = []
  for i in range(min_year, max_year):
    start_urls.append(
      'http://www.pro-football-reference.com/years/' + str(i) + '/games.htm'
    )

  #def __init__(self):
  #  dispatcher.connect(self.spider_closed, signals.spider_closed)

  # Scrapy automatically calls this method, sequentially, for every url in the
  # 'start_urls' array
  #
  # Response is the HTTP response received by Scrapy
  #
  def parse(self, response):
      # Grab and traverse to all links to boxscores
      link_sel = Selector(response)
      links = link_sel.xpath('//a[contains(text(),"boxscore")]/@href').extract()
      for link in links:
        cleaned_url = "http://www.pro-football-reference.com" + link
        yield Request(cleaned_url, callback=self.parse_page)

  # This method is called for every boxscore page. It reads in all of the
  # information from the 'team stats', and prints it to the page. This needs to
  # be modified to store the data instead in a more usefully form like JSON or
  # XML
  #
  # Response is, again, the HTTP response
  #
  def parse_page(self, response):
      sel = Selector(response)

      game_time = sel.xpath('//table[1]/tr/td[1]/node()').extract()

      if str(game_time[0]).split(' ')[0].lower() == 'week':
        # Gets the year and week
        week = int(game_time[0].split(' ')[1])
        year = int(game_time[2])

        # Gets the final scores
        score_table = sel.xpath('//table[@id="linescore"]/tr/td/text()').extract()
        team_one_score = int(score_table[5])
        team_two_score = int(score_table[11])

        team_names = sel.xpath('//table[@id="linescore"]/tr/td/a/text()').extract()
        team_one_name = team_names[0]
        team_two_name = team_names[1]

        margin = team_one_score - team_two_score

        line_team = sel.xpath('//table[@id="game_info"]/tr/td/node()')

        favored_team = ""
        cn = 0
        for l in line_team:
          extract = l.extract()
          if str(extract) == "<b>Vegas Line</b>":
            favored_team = line_team[cn + 1].extract()
          cn = cn + 1



        line = sel.xpath('//table[@id="game_info"]/tr/td/a/node()').extract()
        line_val = float(line[0])

        if str(favored_team).strip() == str(team_one_name).strip():
          line_val = line_val * -1.0

        self.log(str(favored_team))
        self.log(str(team_one_name))
        self.log(str(line_val))
        #item = Margin()
        #item['margin'] = float(margin) - float(line[0])
        item = LinediscrepencyItem()
        item['line'] = line_val
        item['margin'] = margin
        item['week'] = week
        item['year'] = year
        return item
      return None

  #def spider_closed(self):
  #  teams = open('disc.json', 'w')
  #  teams.write(json.dumps(team_dictionary, sort_keys=True,separators=(',',':')))
  #  teams.close()

