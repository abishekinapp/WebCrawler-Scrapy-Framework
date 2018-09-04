# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


#The Items are initialised here

class HinduItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
    subtitle = scrapy.Field()
    image_details = scrapy.Field()
    publish_date = scrapy.Field()
    modified_date = scrapy.Field()
    created_date = scrapy.Field()
    link = scrapy.Field()
    old_post = scrapy.Field()
