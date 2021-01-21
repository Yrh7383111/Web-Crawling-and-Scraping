from scrapy import Spider
from scrapy.http import Request


class AsosSpider(Spider):
    name = 'ASOS'
    allowed_domains = ['asos.com']
    start_urls = ['https://www.asos.com/women/', 'https://www.asos.com/men/']


    def parse(self, response, **kwargs):
        relative_category_links = response.xpath('//a[@class="feature__link"]/@href').extract()
        for relative_category_link in relative_category_links:
            category_link = response.urljoin(relative_category_link)
            yield Request(url=category_link, callback=parse_page)


def parse_page(response):
    category = response.xpath('//h1/text()').extract_first()
    products = response.xpath('//article')
    for product in products:
        img_link = product.xpath('.//img[@data-auto-id="productTileImage"]/@src').extract_first()
        if img_link:
            img_link = 'https:' + img_link
        else:
            img_link = ''
        description = product.xpath('.//div[@data-auto-id="productTileDescription"]//p/text()').extract_first()
        price_tags = product.xpath('.//div[@data-auto-id="productTileDescription"]/following-sibling::p/span/span/text()').extract()
        price = ' '.join(price_tags)
        yield {'Category': category,
               'Description': description,
               'Image Link': img_link,
               'Price': price}

    next_link = response.xpath('//a[@data-auto-id="loadMoreProducts"]/@href').extract_first()
    if next_link:
        yield Request(url=next_link, callback=parse_page)
