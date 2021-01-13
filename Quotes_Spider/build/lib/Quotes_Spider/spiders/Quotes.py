import scrapy



class QuotesSpider(scrapy.Spider):
    name = 'Quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['https://quotes.toscrape.com/']


    def parse(self, response):
        # # Basic spider
        # title = response.xpath('//h1/a/text()').extract()
        # top_ten_tags = response.xpath('//*[@class="tag-item"]/a/text()').extract()
        #
        # yield {'Title': title, 'Top Ten Tags': top_ten_tags}


        # More advanced spider
        quotes = response.xpath('//div[@class="quote"]')

        for quote in quotes:
            text = quote.xpath('./span[@class="text"]/text()').extract_first()
            text = text.lstrip('\“')
            text = text.rstrip('\”')
            author = quote.xpath('./span[2]/small[@class="author"]/text()').extract_first()
            tags = quote.xpath('./div[@class="tags"]/a[@class="tag"]/text()').extract()

            yield {'Text': text, 'Author': author, 'Tags':  tags}

        relative_next_page_url = response.xpath('//li[@class="next"]/a/@href').extract_first()
        absolute_next_page_url = response.urljoin(relative_next_page_url)
        # Do not save value in memory - better memory efficiency
        yield scrapy.Request(url=absolute_next_page_url, callback=self.parse)
