#coding=utf-8
import scrapy
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request, FormRequest
class ITjuziSpider(CrawlSpider):
    name = "itjuzi"
    allowed_domains = ["itjuzi.com"]
    start_urls = ["http://itjuzi.com/"]
    rules = (`请输入代码`
        Rule(SgmlLinkExtractor(allow = ('investevents', ))),
        Rule(SgmlLinkExtractor(allow=('investevents/\?page\=([\d]+)', ),),callback='parse_item',follow=True),
    )

    headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip,deflate",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Connection": "keep-alive",
    "Content-Type":" application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.76 Safari/537.36",
    "Referer": "http://itjuzi.com/"
    }

    def start_requests(self):
        return [Request("http://itjuzi.com/user/login", meta = {'cookiejar' : 1}, callback = self.post_login)]

    def post_login(self, response):
        print 'Preparing login'
        #FormRequeset.from_response是Scrapy提供的一个函数, 用于post表单
        #登陆成功后, 会调用after_login回调函数
        return [FormRequest.from_response(response,   #"http://www.itjuzi.com/user/login",
                            meta = {'cookiejar' : response.meta['cookiejar']},
                            headers = self.headers,  #注意此处的headers
                            formdata = {
                            'email': '邮箱',
                            'password': '密码'
                            },
                            callback = self.after_login,
                            dont_filter = True
                            )]


    def after_login(self, response) :
        for url in self.start_urls :
            yield self.make_requests_from_url(url)

    def parse_item(self, response):
        sel = Selector(response)
        sites = sel.xpath('//table[@class="children-norml-link"]/tbody/tr')

        items = []
        for site in sites:
            item = ITjuziItem()
            item['time'] = site.select('./td[1]/text()').extract()
            item['company'] = site.select('./td[2]/a/text()').extract()
            item['com_href'] = site.select('./td[2]/a/@href').extract()
            item['turn'] = site.select('./td[3]/a/text()').extract()
            item['money'] = site.select('./td[4]/text()').extract()
            item['area'] = site.select('./td[5]/a/text()').extract()
            item['area_href'] = site.select('./td[5]/a/@href').extract()
            item['invest'] = site.select('./td[6]/a/text()').extract()
            item['inv_href'] = site.select('./td[6]/a/@href').extract()
            items.append(item)
        return items

       运行结果如下：
