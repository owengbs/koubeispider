# -*- coding:utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapydemo.yaolan.yaolan_parser import YaolanParser


class YaolanSpider(CrawlSpider):
    name = "yaolan"
    allowed_domains = [ "ask.yaolan.com", "http://ask.yaolan.com"]
    start_urls = [
        "http://www.babytree.com/ask/myqa__view~mlist,tab~D"
    ]

    rules = [
        # yaolan
        Rule(scrapy.linkextractors.LinkExtractor(
            allow=('http://ask.yaolan.com/period/\d+_\d+.html', 'http://ask.yaolan.com/period/\d+_\d+_\d+.html'), ), ),
        Rule(scrapy.linkextractors.LinkExtractor(allow=('/question/\d+.html',), restrict_xpaths=(
        '//div[@class="ask_list_fr"]/div[@class="ask_list"]/ul/li/div[@class="ask_list_title"]/a',)),
             callback='pare_yaolan'),
    ]

    def pare_yaolan(self, response):
        parser = YaolanParser()
        return parser.parse_page(response)