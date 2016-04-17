# -*- coding:utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
import scrapy
from scrapydemo.items import ScrapydemoItem
from scrapydemo.utils.item_helper import ItemHelper


class BabyTreeSpider(CrawlSpider):
    name = "babytree"
    allowed_domains = ["www.babytree.com"]
    _item_helper = ItemHelper()
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
        item = self.parse_question_content(response)
        question_title = item['title']
        items.append(item)
        best_item = self.parse_best_answer(response, question_title)  # best answer
        items.append(best_item)
        answer_items = self.parse_answer_section(response, question_title, response.url, 1)
        items = items + answer_items
        return items

    def parse_anchor_answner_page(self, response):
        detail_selector = Selector(response)
        sels = detail_selector.xpath("//div[@class='qa-article section-module']")
        if len(sels) > 1:
            raise " sels  length is more than one"
        title_selector = sels[0]
        title = title_selector.xpath("./div[@class='qa-title']/h1/text()")[0].extract()
        post_url, pg_number = self.anchor_answer_post_url(response.url)
        items = self.parse_answer_section(response, title, post_url, pg_number)
        return items

    def parse_question_content(self, response):
        detail_selector = Selector(response)
        create_time = detail_selector.xpath('//*[@id="qa-article"]/div[2]/div/span/abbr/@title')[0].extract()
        author_sec = detail_selector.xpath('//*[@id="qa-article"]/div[2]/div/ul/li[1]/a/span[@itemprop="accountName"]/text()')
        author = ''
        if len(author_sec)>0:
            author = author_sec.extract()[0]
        question_section = detail_selector.xpath('//*[@id="qa-article"]/div[1]/h1[@itemprop="title"]/text()').extract()[0]

        content_section = answer.xpath("./div[@class='answer-text']/descendant-or-self::*/text()")
        content = ''
        for each in content_section:
            content = content + each.extract()

        question_item = self._item_helper.build_question(question, create_time, author,
                                         response.url, question, self.allowed_domains[0])

        return question_item

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

        return self._item_helper.build_best_answer(title, create_time, author, response.url,
                                                   response.url, "1", answer_text,
                                                   self.allowed_domains[0])

    # parse answer section
    def parse_answer_section(self, response, title, post_url, pg_number):
        items = list()
        rank = 1 + (pg_number-1)*12
        for answer in response.selector.xpath('//*[@id="qa-answers"]/div[2]/ul/li'):
            author = answer.xpath("./ul[@class='qa-meta']/li[@class='username']/a/span/text()")[0].extract()
            create_time = answer.xpath("./ul[1]/li[3]/abbr/@title")
            if create_time:
                create_time = create_time.extract()[0]
            content_section = answer.xpath("./div[@class='answer-text']/descendant-or-self::*/text()")
            content = ''
            for each in content_section:
                content = content + each.extract()

            answer_item = self._item_helper.build_answer(title, create_time, author,
                                                         response.url, post_url, str(rank),
                                                         content, self.allowed_domains[0])
            rank = rank +1
            items.append(answer_item)
        return items

    # build  question page url
    def anchor_answer_post_url(self, original_url):
        index_begin = original_url.find('qid~') + 4
        index_end = original_url.find(',pg~')
        qid = original_url[index_begin:index_end]
        pg_num = original_url[index_end + 4:]
        url = 'http://www.babytree.com/ask/detail/' + qid
        return url, int(pg_num)