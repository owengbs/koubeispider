#coding=utf-8
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request, FormRequest
class ITjuziSpider(CrawlSpider):
    name = "itjuzi"
    allowed_domains = ["https://www.itjuzi.com"]
    start_urls = ["https://www.itjuzi.com/investfirm?user_id=228677"]
    rules = (
        Rule(SgmlLinkExtractor(allow=('https://www.itjuzi.com/investfirm?user_id=228677&page=\d+', ),),callback='parse_item',follow=True),
    )

    headers = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding":"gzip, deflate",
    "Accept-Language":"zh-CN,zh;q=0.8",
    "Cache-Control":"max-age=0",
    "Connection":"keep-alive",
    "Content-Length":"53",
    "Content-Type":"application/x-www-form-urlencoded",
    "Cookie":"gr_user_id=789b1a6f-614e-4d85-9ef7-b09453c9e261; session=f604470ce54f1286fc980f21870815f0cfd4dfe4; _gat=1; gr_session_id_eee5a46c52000d401f969f4535bdaa78=0797b5c0-01bd-4148-a5c5-6eed3b0a3ad1; Hm_lvt_1c587ad486cdb6b962e94fc2002edf89=1459081786,1459083055,1459171847; Hm_lpvt_1c587ad486cdb6b962e94fc2002edf89=1459171944; _ga=GA1.2.1782217984.1459081786",
    "Host":"www.itjuzi.com",
    "Origin":"https://www.itjuzi.com",
    "Referer":"https://www.itjuzi.com/user/login",
    "Upgrade-Insecure-Requests":"1",
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"
    }

    def start_requests(self):
        print  'start requests .....'
        return [Request("http://www.itjuzi.com/user/login?redirect=investfirm",headers=self.headers,method='POST', meta = {'cookiejar' : 1}, callback = self.post_login)]

    def post_login(self, response):
        print 'Preparing login ... '
        response.url

        return [FormRequest.from_response(response,
                                          meta = {'cookiejar' : response.meta['cookiejar']},
                                          headers = self.headers,
                                          formdata = {
                                              'identity': 'chenshao0594@126.com',
                                              'password': 'Shaoqing@0594'
                                                },
                                          callback = self.after_login,
                                          dont_filter = True
                                          )]


    def after_login(self, response) :
        for url in self.start_urls :
            yield self.make_requests_from_url(url)

    def parse_item(self, response):
        print 'parse item'
        sel = Selector(response)
        sites = sel.xpath('//table[@class="children-norml-link"]/tbody/tr')

        items = []
        for site in sites:
            print site.select('./td[1]/text()').extract()
            print site.select('./td[2]/a/text()').extract()
        return items

