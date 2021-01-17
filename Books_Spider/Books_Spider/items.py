# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BooksSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Title = scrapy.Field()
    Price = scrapy.Field()
    Rating = scrapy.Field()
    Img_URL = scrapy.Field()
    Description = scrapy.Field()
    UPC = scrapy.Field()
    Product_Type = scrapy.Field()
    Price_Exclude_Tax = scrapy.Field()
    Price_Include_Tax = scrapy.Field()
    Tax = scrapy.Field()
    Availability = scrapy.Field()
    Number_of_Reviews = scrapy.Field()
