#from scrapy.spider import CrawlSpider
from scrapy.selector import Selector
from scrapy.http.request import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

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
  max_year = 2012

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
      # This prints all the table data
      for row in table:
        self.log(row)

      return None


