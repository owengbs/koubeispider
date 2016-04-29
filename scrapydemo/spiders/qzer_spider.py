
import scrapy
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from scrapydemo.qzer.qzer_parser import QzerParser


class QzerSpider(CrawlSpider):
    name = "qzer"
    allowed_domains = ['17qzer.com']
    custom_settings = {
                       'CONCURRENT_REQUESTS': 10,
                       'CONCURRENT_REQUESTS_PER_IP': 10,
                       'AUTOTHROTTLE_ENABLED': True,
                       'RETRY_TIMES': 10,
                       }

    start_urls = [

        'http://www.17qzer.com/forum-54-1.html',
        'http://www.17qzer.com/forum-55-1.html',
        'http://www.17qzer.com/forum-2-1.html',
        'http://www.17qzer.com/forum-37-1.html',
        'http://www.17qzer.com/forum-36-1.html',
        'http://www.17qzer.com/forum-39-1.html',
        'http://www.17qzer.com/forum-40-1.html',
        'http://www.17qzer.com/forum-41-1.html',
        'http://www.17qzer.com/forum-42-1.html',
        'http://www.17qzer.com/forum-46-1.html',
        'http://www.17qzer.com/forum-47-1.html',
        'http://www.17qzer.com/forum-48-1.html',
        'http://www.17qzer.com/forum-49-1.html',
        'http://www.17qzer.com/forum-51-1.html',
        'http://www.17qzer.com/forum-60-1.html',
        'http://www.17qzer.com/forum-58-1.html',
        'http://www.17qzer.com/forum-59-1.html',
        'http://www.17qzer.com/forum-57-1.html',
        'http://www.17qzer.com/forum-62-1.html',
        'http://www.17qzer.com/forum-61-1.html',
        'http://www.17qzer.com/forum-56-1.html',
        'http://www.17qzer.com/forum-64-1.html',
        'http://www.17qzer.com/forum-65-1.html',
        'http://www.17qzer.com/forum-66-1.html',
        'http://www.17qzer.com/forum-67-1.html',
        'http://www.17qzer.com/forum-68-1.html',
        'http://www.17qzer.com/forum-69-1.html',
        'http://www.17qzer.com/forum-70-1.html',
        'http://www.17qzer.com/forum-71-1.html',

    ]

    rules = (
        #  paging
        Rule(scrapy.linkextractors.LinkExtractor(allow=('http://www.17qzer.com/forum-\d+-\d+.html',),
                                                 restrict_xpaths=(
                                                 '//*[@id="fd_page_bottom"]/div/a',)), ),

        # detail page
        Rule(scrapy.linkextractors.LinkExtractor(allow=('http://www.17qzer.com/thread-\d+-\d+-\d+.html',),
                                                 restrict_xpaths=('//a[@class="s xst"]',)),
             follow=True, callback='parse_detail_page'),


        Rule(scrapy.linkextractors.LinkExtractor(allow=('http://www.17qzer.com/thread-\d+-\d+-\d+.html',),
                                                 restrict_xpaths=('//div[@class="pg"]/a',)),
             follow=True, callback='parse_detail_page'),

    )

    def parse_detail_page(self, response):
        parser = QzerParser()
        return parser.parse_page(response)
