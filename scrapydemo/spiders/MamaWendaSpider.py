# -*- coding:utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
import scrapy

from scrapydemo.mamawenda.mamawenda_parser import MamawendaParser


class MamaWendaSpider(CrawlSpider):
    name = "mamawenda"
    allowed_domains = ["www.mamawenda.cn"]
    start_urls = [
        'http://www.mamawenda.cn/article/ask?&p=1',
        'http://www.mamawenda.cn/ask/category',
    ]
    rules = (

        Rule(scrapy.linkextractors.LinkExtractor(allow=('http://www.mamawenda.cn/article/ask\?&p=\d+',), )),

        Rule(scrapy.linkextractors.LinkExtractor(allow=('http://www.mamawenda.cn/ask/list/s0t\d+',),
                                                 restrict_xpaths=('//*[@id="conts_wrap"]/div[2]/div[1]/ul/li/dl/dt/a'))),
        Rule(scrapy.linkextractors.LinkExtractor(allow=('http://www.mamawenda.cn/ask/list/s0t\d+p\d+',), )),
        Rule(scrapy.linkextractors.LinkExtractor(allow=('http://www.mamawenda.cn/article/view/\d+',),
                                                  restrict_xpaths=('//*[@id="conts_wrap"]/div[2]/div[1]/div[2]/ul[@class="j_list"]/li/p/a')),
              follow=True, callback='parse_detail'),


        Rule(scrapy.linkextractors.LinkExtractor(allow=('http://www.mamawenda.cn/ask/a/\d+',),),
              follow=True, callback='parse_wenda_detail'),

    )


    def parse_detail(self, response):
        parser = MamawendaParser()
        return parser.parse_page(response)


    def parse_wenda_detail(self, response):
        parser = MamawendaParser()
        return parser.parse_wenda_page(response)
