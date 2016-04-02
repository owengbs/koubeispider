# -*- coding:utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapydemo.mama.mama_parser import MamaParser
import scrapy

from scrapydemo.muying.muying_parser import MuYingParser


class MuyingSpider(CrawlSpider):
    name = "muying"
    allowed_domains = ["www.23myw.com"]
    start_urls = [
        'http://www.23myw.com/forum-48-1.html', # 妈妈育儿说说
        'http://www.23myw.com/forum-58-1.html', #婚后亲子
        'http://www.23myw.com/forum-51-1.html', #婚后必阅
        'http://www.23myw.com/forum-55-1.html', # 备孕怀孕
        'http://www.23myw.com/forum-57-1.html', # 家有0-6
        'http://www.23myw.com/forum-50-1.html', #育儿食谱大全
        'http://www.23myw.com/forum-37-1.html', #如何育儿资料
        'http://www.23myw.com/forum-38-1.html', #宝宝常见
        'http://www.23myw.com/forum-41-1.html', #女人健康
        'http://www.23myw.com/forum-43-1.html',#养生美食
        'http://www.23myw.com/forum-40-1.html', # 生活百科
        'http://www.23myw.com/forum-42-1.html', #养生保健
        'http://www.23myw.com/forum-49-1.html' #家有中小学生

    ]
    rules = (
        Rule(scrapy.linkextractors.LinkExtractor(allow=('http://www.23myw.com/forum-\d+-\d+.html',), )),
        Rule(scrapy.linkextractors.LinkExtractor(allow=('http://www.23myw.com/thread-\d+-\d+-\d+.html',),
                                                 restrict_xpaths=('//*[@id="threadlisttableid"]/tbody/tr/th/a[3]')),
             follow=True, callback='parse_detail'),

    )

    def parse_detail(self, response):
        parser = MuYingParser()
        return parser.parse_page(response)
