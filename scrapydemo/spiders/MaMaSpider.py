# -*- coding:utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapydemo.items import ScrapydemoItem
from scrapydemo.mama.mama_parser import MamaParser
from scrapydemo.yaolan.yaolan_parser import YaolanParser
import scrapy

class MaMaSpider(CrawlSpider):
    name = "mama"
    allowed_domains = ["www.mama.cn"]
    start_urls = [
        "http://www.mama.cn/ask/list/c0-s101-all-p2.html",
    ]
    rules = (
        Rule(scrapy.linkextractors.LinkExtractor(allow=('http://www.mama.cn/ask/list/c0-s\d+-all-p\d+.html',), )),
        Rule(scrapy.linkextractors.LinkExtractor(allow=('http://www.mama.cn/ask/q\d+-p\d+.html',),
                                                 restrict_xpaths=(
                                                     '//ul[@class="aFilter"]/li/div[@class="aCon"]/p[@class="htitle"]/a',
                                                     '//div[@class="pagination"]/div[@class="pg"]/a')),
             follow=True, callback='parse_mama_detail'),

    )
    def parse_mama_detail(self, response):
        parser = MamaParser()
        return parser.parse_page(response)