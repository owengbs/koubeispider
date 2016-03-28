# -*- coding:utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapydemo.items import ScrapydemoItem
import scrapy


class DmozSpider(CrawlSpider):
    name = "babytree"
    allowed_domains = ["www.babytree.com"]
    start_urls = [
        "http://www.babytree.com/ask/myqa__view~mlist,tab~D"
    ]

    rules = (
        #  www.babytree.com
        Rule(scrapy.linkextractors.LinkExtractor(allow=('http://www.babytree.com/ask/myqa__view~mlist,tab~D,pg~\d+', ),)),
        Rule(scrapy.linkextractors.LinkExtractor(allow=('http://www.babytree\.com/ask/detail/\d+', ),restrict_xpaths=('//ul/li[@class="list-item"]/p[@class="list-title"]/a',)) ,
                follow=True, callback='parse_detail_page'),
        Rule(scrapy.linkextractors.LinkExtractor(allow=('http://www.babytree.com/ask/myqa__view~qdetail,qid~\d+,pg~\d+#anchor_answer', ),),
                callback='parse_anchor_answner_page'),

    )

    def parse_detail_page(self, response):
        if response.body.strip() == "":
            print 'empty body url:' + response.url
            return
        items = list()
        item = self.parse_title_content(response)
        question_title = item['title']
        items.append(item)
        best_item = self.parse_best_answer(response, question_title)  # best answer
        items.append(best_item)
        answer_items = self.parse_answer_section(response, question_title, response.url)
        items = items + answer_items
        return items

    def parse_anchor_answner_page(self, response):
        print 'parse anchor answer page: ' + response.url
        detail_selector = Selector(response)
        sels = detail_selector.xpath("//div[@class='qa-article section-module']")
        if len(sels) > 1:
            raise " sels  length is more than one"
        title_selector = sels[0]
        title = title_selector.xpath("./div[@class='qa-title']/h1/text()")[0].extract()
        post_url = self.anchor_answer_post_url(response.url)
        items = self.parse_answer_section(response, title, post_url)
        return items

    def parse_title_content(self, response):
        item = ScrapydemoItem()
        detail_selector = Selector(response)
        sels = detail_selector.xpath("//div[@class='qa-article section-module']")
        if len(sels) > 1:
            raise " sels  length is more than one"
        title_selector = sels[0]
        title = title_selector.xpath("./div[@class='qa-title']/h1/text()")[0].extract()
        item['title'] = title
        item['create_time'] = title_selector.xpath(
            "./div[@class='qa-related']/div[@class='qa-contributor']/span[@class='source']/span[@itemprop='post_time']/text()")[
            0].extract()
        item['author'] = ''
        author_selectors = title_selector.xpath(
            "./div[@class='qa-related']/div[@class='qa-contributor']/ul/li/a/span/text()")
        if len(author_selectors) == 1:
            item['author'] = author_selectors[0].extract()
        item['from_url'] = response.url
        item['post_url'] = response.url
        item['rank'] = "0"
        item['content_type'] = "0"
        item['content'] = title
        item['is_best'] = '0'
        item['domain'] = self.allowed_domains[0]
        return item

    def parse_best_answer(self, response, title):
        best_answers = response.selector.xpath(
            "//div[@id='qa-answer-best']/div[@class='module-content']/div[@class='best-content']")
        if len(best_answers) == 0:
            return None
        elif len(best_answers) > 1:
            raise 'more than one best answer'
        bes = best_answers[0]
        texts = bes.xpath("./div[@class='answer-text']/text()").extract()
        answer_text = texts[0]
        if len(texts) > 1:
            a = bes.xpath("./div[@class='answer-text']/a/text()").extract()
            if len(a) > 0:
                answer_text = answer_text + a[0]
            answer_text = answer_text + texts[1]
        create_time = bes.xpath("./ul[@class='qa-meta']/li[@class='timestamp']/span/text()").extract()[0]
        author = bes.xpath(
            "./div[@class='answer-related']/div[@class='qa-contributor']/ul/li/a/span[@itemprop='accountName']/text()").extract()[
            0]

        return self.build_item(title, create_time, author, response.url, response.url, "", "1", answer_text, "1",
                               self.allowed_domains[0])

    # parse answer section
    def parse_answer_section(self, response, title, post_url):
        items = list()
        for answer in response.selector.xpath("//ul[@class='qa-answer-list']/li[@class='answer-item']"):
            author = answer.xpath("./ul[@class='qa-meta']/li[@class='username']/a/span/text()")[0].extract()
            create_time = \
            answer.xpath("./ul[@class='qa-meta']/li[@class='timestamp']/span[@itemprop='reply_time']/text()")[
                0].extract()
            content = answer.xpath("./div[@class='answer-text']/text()")[0].extract()

            answer_item = self.build_item(title, create_time, author, response.url, post_url, "", "1", content, "0",
                                          self.allowed_domains[0])
            items.append(answer_item)
        return items

    # build  question page url
    def anchor_answer_post_url(self, original_url):
        index_begin = original_url.find('qid~') + 4
        index_end = original_url.find(',pg~')
        qid = original_url[index_begin:index_end]
        url = 'http://www.babytree.com/ask/detail/' + qid
        return url

    def build_item(self, title, create_time, author, from_url, post_url, rank, content_type, content, is_best, domain):
        item = ScrapydemoItem()
        item['title'] = title
        item['create_time'] = create_time
        item['author'] = author
        item['from_url'] = from_url
        item['post_url'] = post_url
        item['rank'] = rank
        item['content_type'] = content_type
        item['content'] = content
        item['is_best'] = is_best
        item['domain'] = domain
        return item

