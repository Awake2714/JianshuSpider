# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JianshuItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    publish_time = scrapy.Field()
    words = scrapy.Field()
    views = scrapy.Field()
    url = scrapy.Field()
    likes = scrapy.Field()
    dislikes = scrapy.Field()
    author = scrapy.Field()