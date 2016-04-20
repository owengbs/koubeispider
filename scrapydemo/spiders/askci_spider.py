import urlparse

import scrapy
from scrapydemo.ask_ci.askci_parser import AskCiParser

class AskCISpider(scrapy.Spider):
    name = "askci"
    allowed_domains = ["ask.ci123.com"]
    _base_url = 'http://ask.ci123.com'
    start_urls = [
        'http://ask.ci123.com/categories/show/2',
        'http://ask.ci123.com/categories/show/3',
        'http://ask.ci123.com/categories/show/4',
        'http://ask.ci123.com/categories/show/5',
        'http://ask.ci123.com/categories/show/6',
        'http://ask.ci123.com/categories/show/7',
        'http://ask.ci123.com/categories/show/8',
        'http://ask.ci123.com/categories/show/9',
        'http://ask.ci123.com/categories/show/10',
        'http://ask.ci123.com/categories/show/11',
        'http://ask.ci123.com/categories/show/12',
        'http://ask.ci123.com/categories/show/13',
        'http://ask.ci123.com/categories/show/14',
        'http://ask.ci123.com/categories/show/15',
        'http://ask.ci123.com/categories/show/16',
        'http://ask.ci123.com/categories/show/17',
        'http://ask.ci123.com/categories/show/18',
        'http://ask.ci123.com/categories/show/19',
        'http://ask.ci123.com/categories/show/20',
        'http://ask.ci123.com/categories/show/42',
        'http://ask.ci123.com/categories/show/43',
        'http://ask.ci123.com/categories/show/44',
        'http://ask.ci123.com/categories/show/45',
        'http://ask.ci123.com/categories/show/26',
        'http://ask.ci123.com/categories/show/46',
        'http://ask.ci123.com/categories/show/2754',
    ]
    def parse(self, response):
        self.parse_question_datetime(response)
        for question_url in response.xpath('//*[@id="list_ask_middle2"]/div/div[1]/div/ul[2]/li/a[1]/@href').extract():
            question_url = urlparse.urljoin(self._base_url, question_url)
            yield scrapy.Request(question_url, callback=self.parse_answers)

        for url in response.xpath('//*[@id="list_page"]/div/a/@href').extract():
            url = urlparse.urljoin(self._base_url, url)
            yield scrapy.Request(url, callback=self.parse)

    # parse question in paging page
    def parse_question_datetime(self, response):
        parser = AskCiParser()
        return parser.parse_question_datetime(response)

    # parse answer page
    def parse_answers(self, response):
        parser = AskCiParser()
        return parser.parse_answers(response)