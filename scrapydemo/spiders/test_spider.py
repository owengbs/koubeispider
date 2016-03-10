# -*- coding:utf-8 -*-
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapydemo.items import ScrapydemoItem


class DmozSpider(CrawlSpider):

    name = "test"
    allowed_domains = ["www.babytree.com"]
    start_urls = [
        "http://www.babytree.com/ask/myqa__view~mlist,tab~D,pg~3",
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=('http://www.babytree.com/ask/myqa__view~mlist,tab~D,pg~\d+', ),)),
        Rule(SgmlLinkExtractor(allow=('http://www.babytree\.com/ask/detail/\d+', ),restrict_xpaths=('//ul/li[@class="list-item"]/p[@class="list-title"]/a',)) ,follow=True, callback='parse_detail_page'),
        Rule(SgmlLinkExtractor(allow=('http://www.babytree.com/ask/myqa__view~qdetail,qid~\d+,pg~\d+#anchor_answer', ),),callback='parse_anchor_answner_page'),

    )

    def parse_detail_page(self, response):
        if response.body.strip() == "":
            print 'empty body url:' + response.url
            return
        items = list()
        item = self.parse_title_content(response)
        items.append(item)
        answer_items = self.parse_answer_section(response, item['title'], response.url)
        items = items + answer_items
        return items

    def parse_title_content(self,response):
        item = ScrapydemoItem()
        detail_selector = Selector(response)
        sels = detail_selector.xpath("//div[@class='qa-article section-module']")
        if len(sels) >1:
            raise " sels  length is more than one"
        title_selector = sels[0]
        title = title_selector.xpath("./div[@class='qa-title']/h1/text()")[0].extract()
        item['title'] = title
        item['create_time'] = title_selector.xpath("./div[@class='qa-related']/div[@class='qa-contributor']/span[@class='source']/span[@itemprop='post_time']/text()")[0].extract()
        item['author'] = ''
        author_selectors = title_selector.xpath("./div[@class='qa-related']/div[@class='qa-contributor']/ul/li/a/span/text()")
        if len(author_selectors)==1:
            item['author'] = author_selectors[0].extract()
        item['from_url'] = response.url
        item['post_url'] = response.url
        item['rank'] = "0"
        item['content_type'] = "0"
        item['content'] = title
        return item

    def parse_answer_section(self, response, title, post_url):
        items = list()
        for answer in response.selector.xpath("//ul[@class='qa-answer-list']/li[@class='answer-item']"):
            answer_item = ScrapydemoItem()
            answer_item['title'] = title
            answer_item['author'] = answer.xpath("./ul[@class='qa-meta']/li[@class='username']/a/span/text()")[0].extract()
            answer_item['create_time'] = answer.xpath("./ul[@class='qa-meta']/li[@class='timestamp']/span[@itemprop='reply_time']/text()")[0].extract()
            answer_item['from_url'] = response.url
            answer_item['post_url'] = post_url
            answer_item['rank'] = " "
            answer_item['content_type'] = "1"
            answer_item['content'] = answer.xpath("./div[@class='answer-text']/text()")[0].extract()
            items.append(answer_item)
        return items



    def parse_anchor_answner_page(self , response):
        print 'parse anchor answer page: ' + response.url
        detail_selector = Selector(response)
        sels = detail_selector.xpath("//div[@class='qa-article section-module']")
        if len(sels) >1:
            raise " sels  length is more than one"
        title_selector = sels[0]
        title = title_selector.xpath("./div[@class='qa-title']/h1/text()")[0].extract()
        post_url = self.anchor_answer_post_url(response.url)
        items = self.parse_answer_section(response, title, post_url)
        return items


    def anchor_answer_post_url(self, original_url):
        index_begin = original_url.find('qid~')+4
        index_end=original_url.find(',pg~')
        qid = original_url[index_begin:index_end]
        url = 'http://www.babytree.com/ask/detail/'+qid
        return url

