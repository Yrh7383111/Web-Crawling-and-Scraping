from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor



class LinkSpider(CrawlSpider):
    name = 'Link'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com']
    rules = [Rule(link_extractor=LinkExtractor(), callback='parse', follow=False)]


    def parse(self, response):
        print(response)
