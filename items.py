# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CraigslistScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    ad_link = scrapy.Field()
    date = scrapy.Field()
    neighborhood = scrapy.Field()
    lat = scrapy.Field()
    lon = scrapy.Field()