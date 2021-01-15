from scrapy import Spider
from scrapy.http import Request


# Extract information of each book
def parse_book(response):
    # Basic information
    title = response.xpath('//h1/text()').extract_first()
    price = response.xpath('//p[@class="price_color"]/text()').extract_first()
    price = price[1:]
    rating = response.xpath('//p[contains(@class, "star-rating")]/@class').extract_first()
    rating = rating.replace('star-rating ', '')
    img_url = response.xpath('//div[contains(@class, "item") and contains(@class, "active")]/img/@src').extract_first()
    img_url = img_url.replace('../..', 'https://books.toscrape.com')
    description = response.xpath('//body/div[1]/div[1]/div[2]/div[2]/article[1]/p[1]/text()').extract_first()

    # Product information
    header_list = []
    data_list = []
    trs = response.xpath('//tr')
    for tr in trs:
        header = tr.xpath('./th/text()').extract_first()
        data = tr.xpath('./td/text()').extract_first()
        if header == 'Price (excl. tax)':
            data = data[1:]
        if header == 'Price (incl. tax)':
            data = data[1:]
        if header == 'Tax':
            data = data[1:]
        header_list.append(header)
        data_list.append(data)

    result = {'Title': title,
              'Price': price,
              'Rating': rating,
              'Img URL': img_url,
              'Description': description}
    for header, data in zip(header_list, data_list):
        result[header] = data
    yield result


class BooksSpider(Spider):
    name = 'Books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        books = response.xpath('//article[@class="product_pod"]')
        # Check each book
        for book in books:
            relative_book_link = book.xpath('./h3/a/@href').extract_first()
            book_link = response.urljoin(relative_book_link)
            yield Request(url=book_link, callback=parse_book)

        # Go to next page
        relative_next_page_link = response.xpath('//a[contains(text(),"next")]/@href').extract_first()
        next_page_link = response.urljoin(relative_next_page_link)
        yield Request(url=next_page_link, callback=self.parse)
