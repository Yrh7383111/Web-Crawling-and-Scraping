import scrapy



class TabularDataSpider(scrapy.Spider):
    name = 'Tabular_Data'
    allowed_domains = ['en.wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/Walt_Disney_World#Timeline']


    def parse(self, response):
        table = response.xpath('//body/div[@id="content"]/div[@id="bodyContent"]/div[@id="mw-content-text"]/div[1]/table[7]')
        tbody = table.xpath('./tbody')
        trs = tbody.xpath('./tr')

        for tr in trs:
            row = tr.xpath('./td/text()').extract()
            print(*row)
