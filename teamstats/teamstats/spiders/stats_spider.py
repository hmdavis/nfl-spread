import json
#from scrapy.spider import CrawlSpider
from scrapy.selector import Selector
from scrapy.http.request import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

from teamstats.items import GameItem
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
  name = 'teamstatsspider'
  allowed_domains = ['pro-football-reference.com']

  # The range of years (these can later be added as parameters)
  min_year = 1998
  max_year = 2013

  # Develop the start urls based on the years
  start_urls = []
  for i in range(min_year, max_year):
    start_urls.append(
      'http://www.pro-football-reference.com/years/' + str(i) + '/games.htm'
    )

  def __init__(self):
    dispatcher.connect(self.spider_closed, signals.spider_closed)

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
        margin = team_one_score - team_two_score

        # Gets each team!
        thead = sel.xpath('//table[@id="team_stats"]/tr/th/node()').extract()
        team_one = thead[0]
        team_two = thead[1]

        # Add the team to the dictionary if need be
        if team_one not in team_dictionary:
          team_dictionary[team_one] = {}
        if team_two not in team_dictionary:
          team_dictionary[team_two] = {}

        # Add the year to the dictionary if need be
        if year not in team_dictionary[team_one]:
          team_dictionary[team_one][year] = {}
        if year not in team_dictionary[team_two]:
          team_dictionary[team_two][year] = {}

        defensive_stats_one = {}
        defensive_stats_two = {}

        ptable = sel.xpath('//table[@id="skill_stats"]/tbody/tr/node()').extract()

        cn = 0
        team_one_roster = []
        team_two_roster = []

        # grabs the individual players from the Passing, Rushing, & Receiving table
        for skill in ptable:
          if cn % 33 == 10:
            if ("td" in skill):
              st = skill[66:]
              st = st.replace("</a></td>", "")
              team_two_roster.append(st)
          if cn % 33 == 1:
            if ("align=\"left\"" in skill):
              st = skill[66:]
              st = st.replace("</a></td>", "")
              team_one_roster.append(st)
          cn = cn + 1

      defensive_stats_one['roster'] = team_one_roster
      defensive_stats_two['roster'] = team_two_roster
      defensive_stats_one['margin'] = margin
      defensive_stats_two['margin'] = -margin

      # Get the team stats data and save the defensive stuff
      table = sel.xpath('//table[@id="team_stats"]/tr/td/node()').extract()
      counter = 0
      for row in table:
        row_num = ceil(counter / 3)
        col_num = counter % 3
        if col_num == 1:
          if row_num == 0:
            defensive_stats_two['first_downs'] = row
          elif row_num == 1:
            split = row.split("-")
            defensive_stats_two['rush_attempts'] = split[0]
            defensive_stats_two['rush_yards'] = split[1]
            defensive_stats_two['rush_TDs'] = split[2]
          elif row_num == 2:
            split = row.split("-")
            defensive_stats_two['completions'] = split[0]
            defensive_stats_two['attempts'] = split[1]
            defensive_stats_two['passing_yards'] = split[2]
            defensive_stats_two['passing_TDs'] = split[3]
            defensive_stats_two['passing_INTs'] = split[4]
          elif row_num == 3:
            split = row.split("-")
            defensive_stats_two['sacks'] = split[0]
            defensive_stats_two['sack_yards'] = split[1]
          elif row_num == 4:
            defensive_stats_two['net_pass_yards'] = row
          elif row_num == 5:
            defensive_stats_two['net_yards'] = row
          elif row_num == 6:
            split = row.split("-")
            defensive_stats_two['fumbles'] = split[0]
            defensive_stats_two['fumbles_lost'] = split[1]
          elif row_num == 7:
            defensive_stats_two['turnovers'] = row
          elif row_num == 8:
            split = row.split("-")
            defensive_stats_two['penalties'] = split[0]
            defensive_stats_two['penalty_yards'] = split[1]
          else:
            pass
        elif col_num == 2:
          if row_num == 0:
            defensive_stats_one['first_downs'] = row
          elif row_num == 1:
            split = row.split("-")
            defensive_stats_one['rush_attempts'] = split[0]
            defensive_stats_one['rush_yards'] = split[1]
            defensive_stats_one['rush_TDs'] = split[2]
          elif row_num == 2:
            split = row.split("-")
            defensive_stats_one['completions'] = split[0]
            defensive_stats_one['attempts'] = split[1]
            defensive_stats_one['passing_yards'] = split[2]
            defensive_stats_one['passing_TDs'] = split[3]
            defensive_stats_one['passing_INTs'] = split[4]
          elif row_num == 3:
            split = row.split("-")
            defensive_stats_one['sacks'] = split[0]
            defensive_stats_one['sack_yards'] = split[1]
          elif row_num == 4:
            defensive_stats_one['net_pass_yards'] = row
          elif row_num == 5:
            defensive_stats_one['net_yards'] = row
          elif row_num == 6:
            split = row.split("-")
            defensive_stats_one['fumbles'] = split[0]
            defensive_stats_one['fumbles_lost'] = split[1]
          elif row_num == 7:
            defensive_stats_one['turnovers'] = row
          elif row_num == 8:
            split = row.split("-")
            defensive_stats_one['penalties'] = split[0]
            defensive_stats_one['penalty_yards'] = split[1]
          else:
            pass
        else:
          pass
        counter = counter + 1


      team_dictionary[team_one][year][week] = defensive_stats_one
      team_dictionary[team_two][year][week] = defensive_stats_two



      '''# THIS GRABS THE TABLE SPECIFICALLY WITH ID 'TEAM_STATS'. MODIFY THIS TO
      # GET ANY OTHER TABLE
      thead = sel.xpath('//table[@id="team_stats"]/tr/th/node()').extract()
      table = sel.xpath('//table[@id="team_stats"]/tr/td/node()').extract()

      counter = 0
      # Create the game item
      team_item_one= GameItem()
      team_item_one['team_one'] = team_one
      team_item_one['team_two'] = team_two

      cn = 0
      team_one_roster = []
      team_two_roster = []

      # grabs the individual players from the Passing, Rushing, & Receiving table
      for skill in ptable:
        if cn % 33 == 10:
          if ("td" in skill):
            st = skill[66:]
            st = st.replace("</a></td>", "")
            team_two_roster.append(st)
        if cn % 33 == 1:
          if ("align=\"left\"" in skill):
            st = skill[66:]
            st = st.replace("</a></td>", "")
            team_one_roster.append(st)
        cn = cn + 1

      team_item_one['roster_one'] = team_one_roster
      team_item_one['roster_two'] = team_two_roster

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
        counter = counter + 1'''
        #self.log(row)'''


      #return team_item_one

  def spider_closed(self):
    teams = open('teams.json', 'w')
    teams.write(json.dumps(team_dictionary, sort_keys=True,separators=(',',':')))
    teams.close()



