from scrapy import Spider
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser



class LoginSpider(Spider):
    name = 'Login'
    allowed_domains = ['quotes.toscrape.com/']
    start_urls = ['http://quotes.toscrape.com/login/']


    def parse(self, response):
        csrf_token = response.xpath('//body/div[1]/form[1]/input[1]/@value').extract_first()
        username = 'Yrh7383111'
        password = '123456'

        yield FormRequest(url='https://quotes.toscrape.com/login',
                          formdata={'csrf_token': csrf_token,
                                    'username': username,
                                    'password': password},
                          callback=self.login_callback)

    def login_callback(self, response):
        open_in_browser(response)
