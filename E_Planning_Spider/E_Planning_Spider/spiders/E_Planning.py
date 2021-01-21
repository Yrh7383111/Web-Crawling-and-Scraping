import scrapy
from scrapy.http import Request, FormRequest


class EPlanningSpider(scrapy.Spider):
    name = 'E_Planning'
    allowed_domains = ['eplanning.ie']
    start_urls = ['http://www.eplanning.ie/CarlowCC/searchtypes']

    def parse(self, response, **kwargs):
        relative_received_link = 'SearchListing/RECEIVED'
        received_link = response.urljoin(relative_received_link)
        yield Request(url=received_link, callback=parse_form)

        relative_decision_due_link = 'SearchListing/DUE'
        decision_due_link = response.urljoin(relative_decision_due_link)
        yield Request(url=decision_due_link, callback=parse_form)

        relative_decision_made_link = 'SearchListing/MADE'
        decision_made_link = response.urljoin(relative_decision_made_link)
        yield Request(url=decision_made_link, callback=parse_form)


def parse_form(response):
    form_xpath = '//div[@class="container body-content"]//form'
    form_data = {
        'RdoTimeLimit': '42'
    }
    yield FormRequest.from_response(response=response,
                                    formxpath=form_xpath,
                                    formdata=form_data,
                                    callback=parse_page)


def parse_page(response):
    relative_file_links = response.xpath('//td/a/@href').extract()
    for relative_file_link in relative_file_links:
        file_link = response.urljoin(relative_file_link)
        yield Request(url=file_link, callback=parse_file)

    relative_next_link = response.xpath('//li[@class="PagedList-skipToNext"]//a/@href').extract_first()
    next_link = response.urljoin(relative_next_link)
    yield Request(url=next_link, callback=parse_page)


def parse_file(response):
    agents_style = response.xpath('//input[@title="Show Agents Popup"]/@style').extract_first()
    if 'display: inline' and 'visibility: visible' in agents_style:
        name = process_data(response.xpath('//th[normalize-space()="Name :"]/following-sibling::td/text()').extract_first())
        address = process_data(response.xpath('//th[normalize-space()="Address :"]/following-sibling::td/text()').extract_first())
        phone = process_data(response.xpath('//th[normalize-space()="Phone :"]/following-sibling::td/text()').extract_first())
        fax = process_data(response.xpath('//th[normalize-space()="Fax :"]/following-sibling::td/text()').extract_first())
        email = process_data(response.xpath('//th[normalize-space()="e-mail :"]/following-sibling::td/text()').extract_first())
        address_one = process_data(response.xpath('//th[normalize-space()="Address :"]/following-sibling::td/text()').extract_first())
        address_two = response.xpath('//th[normalize-space()="Address :"]/parent::tr/following-sibling::tr/td/text()')[0:3].extract()
        address = address_one + ' ' + ' '.join(address_two)

        yield {'Name': name,
               'Address': address,
               'Phone': phone,
               'Fax': fax,
               'Email': email}


def process_data(data):
    if data:
        data = data.strip()
    else:
        data = ''
    return data
