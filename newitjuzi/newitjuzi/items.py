# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy




class InstitutionItem(scrapy.Item):
    institutionId = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    news = scrapy.Field()
    pass
