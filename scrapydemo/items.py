# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapydemoItem(scrapy.Item):
    author = scrapy.Field()
    create_time = scrapy.Field()
    from_url = scrapy.Field()
    post_url = scrapy.Field()
    rank = scrapy.Field()
    title = scrapy.Field()
    content_type = scrapy.Field()  # 0: question 1: answer
    content = scrapy.Field()
    is_best = scrapy.Field()  # 0: not, 1: is best
    domain = scrapy.Field()
    pass