# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item,Field

class ScrapydemoItem(scrapy.Item):
    author = scrapy.Field()
    create_time = scrapy.Field()
    from_url=scrapy.Field()
    post_url = scrapy.Field()
    rank = scrapy.Field()
    title=scrapy.Field()
    content_type = scrapy.Field()
    content = scrapy.Field()
<<<<<<< 8c6ca10303b7264b6eb92e82b447877376108b4a
=======
    is_best = scrapy.Field()
    domain = scrapy.Field()
>>>>>>> init ...
    pass
