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

team_dictionary = {}
game_dictionary = {}

class TeamStatsSpider(CrawlSpider):

  # Start-up required params
  name = 'teamstatsspider'
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
        away_score = int(score_table[5])
        home_score = int(score_table[11])
        # home - away
        margin = home_score - away_score

        # Gets each team!
        thead = sel.xpath('//table[@id="team_stats"]/tr/th/node()').extract()
        away_team = thead[0]
        home_team = thead[1]

        # Add the team to the team_dictionary if need be
        if away_team not in team_dictionary:
          team_dictionary[away_team] = {}
        if home_team not in team_dictionary:
          team_dictionary[home_team] = {}

        # Add the year to the team_dictionary if need be
        if year not in team_dictionary[away_team]:
          team_dictionary[away_team][year] = {}
        if year not in team_dictionary[home_team]:
          team_dictionary[home_team][year] = {}

        # Add the year to the game_dictionary if need be
        if year not in game_dictionary:
          game_dictionary[year] = {}

        # Initialize the week in the game_dictionary if need be
        if week not in game_dictionary[year]:
          game_dictionary[year][week] = []

        ptable = sel.xpath('//table[@id="skill_stats"]/tbody/tr')

        away_roster = []
        home_roster = []

        # grabs the individual players to create the roster from the Passing, Rushing, & Receiving table
        for player in ptable:
          player_team = player.xpath('td[2]/text()').extract()
          if player_team != [] and player_team[0] == home_team:
            home_roster.append(player.xpath('td[1]/a/text()').extract()[0])
          elif player_team != [] and player_team[0] == away_team:
            away_roster.append(player.xpath('td[1]/a/text()').extract()[0])

        # Construct the game instance in the game_dictionary
        game_dictionary[year][week].append({
          'home': home_team,
          'away': away_team,
          'home_roster': home_roster,
          'away_roster': away_roster,
          'margin': margin
        })

        # Get the team stats data 
        team_table = sel.xpath('//table[@id="team_stats"]/tr')

        # Store the defensive stats for home and away
        defensive_stats_home, defensive_stats_away = self.generate_defensive_stats(team_table)

        # Set the defensive stats in the team_dictionary
        team_dictionary[home_team][year][week] = defensive_stats_home
        team_dictionary[away_team][year][week] = defensive_stats_away

  def generate_defensive_stats(self,team_table):
    defensive_stats_home = []
    defensive_stats_away = []

    for stat_line in team_table[1:]:
      raw_home_stats = stat_line.xpath('td[3]/text()').extract()[0].split('-')
      raw_away_stats = stat_line.xpath('td[2]/text()').extract()[0].split('-')
      
      # Do the opposite to store defensive stats
      for stat in raw_away_stats:
        defensive_stats_home.append(int(stat))
      for stat in raw_home_stats:
        defensive_stats_away.append(int(stat))

    return defensive_stats_home, defensive_stats_away

  def spider_closed(self):
    teams = open('teams.json', 'w')
    teams.write(json.dumps(team_dictionary, sort_keys=True,separators=(',',':')))
    teams.close()
    games = open('games.json','w')
    games.write(json.dumps(game_dictionary,sort_keys=True,separators=(',',':')))
    games.close()



