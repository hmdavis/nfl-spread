#from scrapy.spider import CrawlSpider
from scrapy.selector import Selector
from scrapy.http.request import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from teamstats.items import GameItem
from math import ceil

# TeamStatsSpider
# Author: ardot
#
# This spider scrapes pro-football-reference.com for data regarding team stats.
# Currently, it gets and prints all team statistics for every game that occured
# in the NFL between the 'min-year' and 'max-year' values
#

class TeamStatsSpider(CrawlSpider):

  # Start-up required params
  name = 'teamstatsspider'
  allowed_domains = ['pro-football-reference.com']

  # The range of years (these can later be added as parameters)
  min_year = 1992
  max_year = 1993

  # Develop the start urls based on the years
  start_urls = []
  for i in range(min_year, max_year):
    start_urls.append(
      'http://www.pro-football-reference.com/years/' + str(i) + '/games.htm'
    )


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



      # THIS GRABS THE TABLE SPECIFICALLY WITH ID 'TEAM_STATS'. MODIFY THIS TO
      # GET ANY OTHER TABLE
      thead = sel.xpath('//table[@id="team_stats"]/tr/th/node()').extract()
      table = sel.xpath('//table[@id="team_stats"]/tr/td/node()').extract()
      # Team names are stored in the table head
      team_one = thead[0]
      team_two = thead[1]
      counter = 0
      # Create the game item
      team_item_one= GameItem()
      team_item_one['team_one'] = team_one
      team_item_one['team_two'] = team_two

      # This prints all the table data
      for row in table:
        row_num = ceil(counter / 3)
        col_num = counter % 3
        if col_num == 1:
          if row_num == 0:
            team_item_one['first_downs_one'] = row
          elif row_num == 1:
            split = row.split("-")
            team_item_one['rush_attempts_one'] = split[0]
            team_item_one['rush_yards_one'] = split[1]
            team_item_one['rush_TDs_one'] = split[2]
          elif row_num == 2:
            split = row.split("-")
            team_item_one['completions_one'] = split[0]
            team_item_one['attempts_one'] = split[1]
            team_item_one['passing_yards_one'] = split[2]
            team_item_one['passing_TDs_one'] = split[3]
            team_item_one['passing_INTs_one'] = split[4]
          elif row_num == 3:
            split = row.split("-")
            team_item_one['sacks_one'] = split[0]
            team_item_one['sack_yards_one'] = split[1]
          elif row_num == 4:
            team_item_one['net_pass_yards_one'] = row
          elif row_num == 5:
            team_item_one['net_yards_one'] = row
          elif row_num == 6:
            split = row.split("-")
            team_item_one['fumbles_one'] = split[0]
            team_item_one['fumbles_lost_one'] = split[1]
          elif row_num == 7:
            team_item_one['turnovers_one'] = row
          elif row_num == 8:
            split = row.split("-")
            team_item_one['penalties_one'] = split[0]
            team_item_one['penalty_yards_one'] = split[1]
          else:
            pass
        elif col_num == 2:
          if row_num == 0:
            team_item_one['first_downs_two'] = row
          elif row_num == 1:
            split = row.split("-")
            team_item_one['rush_attempts_two'] = split[0]
            team_item_one['rush_yards_two'] = split[1]
            team_item_one['rush_TDs_two'] = split[2]
          elif row_num == 2:
            split = row.split("-")
            team_item_one['completions_two'] = split[0]
            team_item_one['attempts_two'] = split[1]
            team_item_one['passing_yards_two'] = split[2]
            team_item_one['passing_TDs_two'] = split[3]
            team_item_one['passing_INTs_two'] = split[4]
          elif row_num == 3:
            split = row.split("-")
            team_item_one['sacks_two'] = split[0]
            team_item_one['sack_yards_two'] = split[1]
          elif row_num == 4:
            team_item_one['net_pass_yards_two'] = row
          elif row_num == 5:
            team_item_one['net_yards_two'] = row
          elif row_num == 6:
            split = row.split("-")
            team_item_one['fumbles_two'] = split[0]
            team_item_one['fumbles_lost_two'] = split[1]
          elif row_num == 7:
            team_item_one['turnovers_two'] = row
          elif row_num == 8:
            split = row.split("-")
            team_item_one['penalties_two'] = split[0]
            team_item_one['penalty_yards_two'] = split[1]
          else:
            pass
        else:
          pass
        counter = counter + 1
        #self.log(row)

      return team_item_one


