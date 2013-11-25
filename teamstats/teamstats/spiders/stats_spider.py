from scrapy.spider import BaseSpider
from scrapy.selector import Selector, HtmlXPathSelector
#from scrapy.contrib.spiders import CrawlSpider, Rule
#from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor


class TeamStatsSpider(BaseSpider):
  name = 'teamstatsspider'

  allowed_domains = ['pro-football-reference.com']
  start_urls = ['http://www.pro-football-reference.com/boxscores/200209050nyg.htm']

  #rule = [Rule(SgmlLinkExtractor(allow=['/200209050nyg.htm']), 'parse_team_stats')]

  def parse(self, response):
    sel = Selector(response)
    thead = sel.xpath('//table[@id="team_stats"]/tr/th/node()').extract()
    table = sel.xpath('//table[@id="team_stats"]/tr/td/node()').extract()

    team_one = thead[0]
    team_two = thead[1]

    self.log(team_one)
    self.log(team_two)

    for row in table:
      self.log(row)
    #team_stat = TeamStatItem()
    #team_stat['team_name'] = table

    self.log('A response from %s just arrived!' % response.url)

    #filename = response.url.split("/")[-2]
    #open(filename, 'wb').write(response.body)

    '''sel = Selector(response)
    table = sel.xpath("//table[@id='team_stats']").extract()
    print table
    team_stat = TeamStatItem()
    return team_stat'''
