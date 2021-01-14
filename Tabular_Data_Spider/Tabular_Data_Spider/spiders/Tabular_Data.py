import scrapy



class TabularDataSpider(scrapy.Spider):
    name = 'Tabular_Data'
    allowed_domains = ['en.wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/Walt_Disney_World#Timeline']


    def parse(self, response):
        table = response.xpath('//body/div[@id="content"]/div[@id="bodyContent"]/div[@id="mw-content-text"]/div[1]/table[7]')
        tbody = table.xpath('./tbody')
        trs = tbody.xpath('./tr')

        for i in range(len(trs)):
            if i != 0:
                row = trs[i].xpath('./td/text()').extract()
                yield {'Year': row[0],
                       'Magic Kingdom': row[1],
                       'Epcot': row[2],
                       'Disney Hollywood Studio': row[3],
                       'Disney Animal Kingdom': row[4],
                       'Overall': row[5]}
