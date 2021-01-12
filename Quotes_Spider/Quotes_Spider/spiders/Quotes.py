import scrapy



class QuotesSpider(scrapy.Spider):
    name = 'Quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['https://quotes.toscrape.com/']


    def parse(self, response):
        title = response.xpath('//h1/a/text()').extract()
        top_ten_tags = response.xpath('//*[@class="tag-item"]/a/text()').extract()

        yield {'Title': title, 'Top Ten Tags': top_ten_tags}
