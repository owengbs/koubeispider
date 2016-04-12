#coding=utf-8
import scrapy
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request, FormRequest


class MySpider(CrawlSpider):

    headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip,deflate",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Connection": "keep-alive",
    "Content-Type":" application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.76 Safari/537.36",
    "Referer": "http://itjuzi.com/"
    }


    rules = (
    Rule(SgmlLinkExtractor(allow=('investevents',))),
    Rule(SgmlLinkExtractor(allow=('investevents/\?page\=([\d]+)',), ), callback='parse_item', follow=True),
    )
    name = 'testspider'
    allowed_domains = ['www.itjuzi.com']
    start_urls = [
        'https://www.itjuzi.com/investfirm',

    ]


    def start_requests(self):
        return [Request("http://itjuzi.com/user/login", meta={'cookiejar': 1}, callback=self.post_login)]


    def post_login(self, response):
        print 'Preparing login'
        # FormRequeset.from_response是Scrapy提供的一个函数, 用于post表单
        # 登陆成功后, 会调用after_login回调函数
        return [FormRequest.from_response(response,  # "http://www.itjuzi.com/user/login",
                                      meta={'cookiejar': response.meta['cookiejar']},
                                      headers=self.headers,  # 注意此处的headers
                                      formdata={
                                          'email': '297314262@qq.com',
                                          'password': '4921110'
                                      },
                                      callback=self.after_login,
                                      dont_filter=True
                                      )]


    def after_login(self, response):
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse(self, response):
        self.log('A response from %s just arrived!' % response.url)

    def make_requests_from_url(self, url):
        req = Request(url, dont_filter=True, headers=self.headers)
        print '................'
        print req._get_body()
        print '>>>>>>>>>>>>>>>>>>>>'
        return req

    def parse_item(self, response):
        print 'parse item'
        print response