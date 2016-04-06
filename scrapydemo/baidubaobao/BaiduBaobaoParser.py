# -*- coding:utf-8 -*-
import urllib2

from scrapy import Selector

from scrapydemo.items import ScrapydemoItem
from lxml import etree

class BaiduBaobaoParser():
    domain ="http://baobao.baidu.com"
    maxNum=100  # the max number of more answer

    def parse_detail_page(self, response):
        if response.body.strip() == "":
            return
        items = list()
        item = self.parse_title_content(response)
        question_title = item['title']
        items.append(item)
        answer_url = self.answer_section_url(response.url)
        answer_items = self.parse_answer_section(response.url, question_title, answer_url)
        items = items + answer_items
        return items



    def parse_title_content(self, response):
        detail_selector = Selector(response)
        question_section = detail_selector.xpath('//*[@id="body"]/div/section/article[@class="grid qb-content"]/div[1]')
        if len(question_section) > 1:
            raise " sels  length is more than one"
        title_selector = question_section[0]
        title = title_selector.xpath("./h2/text()")[1].extract()

        author = title_selector.xpath("./div/a[@class='username']/text()")[0].extract()
        create_time = title_selector.xpath("./div/span[1]")[0].extract()
        url = response.url
        item = self.build_item(title, create_time, author, url, url, "0", "0", "0", "0", self.domain)
        return item



    # parse answer section
    def parse_answer_section(self, from_url, title, req_url):
        lists = list()
        req = urllib2.Request(req_url)
        res = urllib2.urlopen(req)
        page = unicode(res.read(), "utf-8")
        tree = etree.HTML(page)
        nodes = tree.xpath("/html/body/div[@class='answer-detail']")
        for node in nodes:
            author = node.xpath("./div[@class='answer-meta']/a[@class='username']/text()")[0]
            content = node.xpath("./p/text()")[0]
            create_time = node.xpath("./div[@class='answer-meta']/span[@class='time']/text()")[0]
            answer_item = self.build_item(title, create_time, author, from_url, from_url, "", "1", content, "0",
                                          self.domain)
            lists.append(answer_item)
        return lists
    # build  question page url
    def answer_section_url(self, original_url):
        index_begin = original_url.find('/question/') + 10
        index_end = original_url.find('.html')
        qid = original_url[index_begin:index_end]
        url = 'http://baobao.baidu.com/question/ajax/replymore?qid=' + qid+'&pn=0&rn='+str(self.maxNum)
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
