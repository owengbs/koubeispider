import scrapy
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from scrapydemo.kuaiwen.kuaiwen_parser import KuaiwenParser
from scrapydemo.utils.item_helper import ItemHelper


class KuaiwenSpider(CrawlSpider):
    name = "kuaiwen"
    allowed_domains = ['kuaiwen.pcbaby.com.cn']
    _item_helper = ItemHelper()
    start_urls = [
        'http://kuaiwen.pcbaby.com.cn/question/t1/p1.html',
        'http://kuaiwen.pcbaby.com.cn/question/t2/p1.html',
        'http://kuaiwen.pcbaby.com.cn/question/t3/p1.html',
        'http://kuaiwen.pcbaby.com.cn/question/t4/p1.html',
        'http://kuaiwen.pcbaby.com.cn/question/t5/p1.html',
        'http://kuaiwen.pcbaby.com.cn/question/t6/p1.html',
        'http://kuaiwen.pcbaby.com.cn/question/t7/p1.html',
        'http://kuaiwen.pcbaby.com.cn/question/t8/p1.html',
        'http://kuaiwen.pcbaby.com.cn/question/t9/p1.html',
        'http://kuaiwen.pcbaby.com.cn/question/t10/p1.html',
        'http://kuaiwen.pcbaby.com.cn/question/t11/p1.html',
        'http://kuaiwen.pcbaby.com.cn/question/t30161/p1.html',
    ]

    rules = (
        #  paging
        Rule(scrapy.linkextractors.LinkExtractor(allow=('http://kuaiwen.pcbaby.com.cn/question/t\d+/p\d+.html',),
                                                 restrict_xpaths=(
                                                 '//div[@class="pcbaby-page mb10"]/a',)), ),

        # detail page
        Rule(scrapy.linkextractors.LinkExtractor(allow=('http://kuaiwen.pcbaby.com.cn/question/\d+.html',),
                                                 restrict_xpaths=('//li/p[@class="pQ"]/a',)),
             follow=True, callback='parse_detail_page'),

    )

    def parse_detail_page(self, response):
        print ' parse_detail_page .... '
        parser = KuaiwenParser()
        parser.parse_page(response)
