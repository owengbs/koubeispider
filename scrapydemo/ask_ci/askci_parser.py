# -*- coding:utf-8 -*-
from scrapy import Selector
from scrapydemo.utils.itemhelper import ItemHelper

from scrapydemo.utils.datetime_helper import DatetimeHelper

from scrapydemo.ask_ci.url_helper import ParseHelper

class AskCiParser(object):
    domain = "http://ask.ci123.com"
    def __init__(self):
        self._helper = ItemHelper()
        self._parse_helper = ParseHelper()

    def parse_question_datetime(self, response):
        page_selector = Selector(response)
        question_section = page_selector.xpath('//*[@id="list_ask_middle2"]/div/div[1]/div/ul[2]/li')
        for each_question in question_section:
            detail_url = each_question.xpath('./a/@href').extract()[0]
            question_time_section = each_question.xpath('./span[@class="list_time"]/text()').extract()
            if len(question_time_section) == 0:
                print 'without question_time, ', detail_url
                continue
            question_time = question_time_section[0]
            self._parse_helper.insert_datetime(detail_url, question_time)
        return None

    def parse_answers(self, response):
        req_url = response.url
        item_list = list()
        page_selector = Selector(response)
        sels = page_selector.xpath('//*[@id="ask_middle2"]/div[5]/div[@class="ask2_inner"]')
        question_item = self._parse_question(sels[0], req_url);
        item_list.append(question_item)
        question = question_item['title']
        best_item = self._parse_best_answer( question, page_selector, response.url)
        if best_item:
            item_list.append(best_item)
        del sels[0]
        for index, each in enumerate(sels):
            answer = self._parse_answer(each, question, str(index+1), req_url )
            item_list.append(answer)
        return item_list


    def _parse_question(self, section, url):
        question = ''
        question_section = section.xpath('./ul[2]/table/tbody/tr[1]/td[2]/h3/text()').extract()
        if len(question_section)>0:
            question = question_section[0]
        content_section = section.xpath('./ul[2]/table/tbody/tr[1]/td[2]/span/descendant-or-self::*/text()')
        content = ''
        for each in content_section:
            content = content + each.extract()
        author = self._build_author(section, './ul[2]/table/tbody/tr[1]/td[1]/p[1]/a/text()')
        create_time = self._parse_helper.get_datetime(url+ParseHelper.suffix)
        question_item = self._helper.build_question(question, DatetimeHelper.build_datetime_str(create_time), author, url, content, self.domain)
        return question_item


    def _parse_best_answer(self, question, page_selector, url):
        best_section = page_selector.xpath('//*[@id="ask_middle2"]/div[5]/div/div[@class="ask2_inner"]')
        if len(best_section)==0:
            return None
        content_section = best_section.xpath('./ul[2]/table/tbody/tr[1]/td[2]/span/descendant-or-self::*/text()')
        content = ''
        for each in content_section:
            content = content + each.extract()

        author = self._build_author(best_section,'./ul[2]/table/tbody/tr[1]/td[1]/p[1]/a/text()')

        create_time = best_section.xpath('./ul[2]/table/tbody/tr[2]/td/p/text()').extract()[0]
        create_time = DatetimeHelper.build_datetime_str(create_time)
        best_item = self._helper.build_best_answer(question, create_time, author, url, url, '1', content, self.domain)
        return best_item


    def _parse_answer(self, section, question, rank, url):
        content_section = section.xpath('./ul[2]/table/tbody/tr[1]/td[2]/span/descendant-or-self::*/text()')
        content = ''
        for each in content_section:
            content = content + each.extract()
        author = self._build_author(section, './ul[2]/table/tbody/tr[1]/td[1]/p[1]/a/text()')
        create_time = section.xpath('./ul[2]/table/tbody/tr[2]/td/p/text()').extract()[0]
        create_time = DatetimeHelper.build_datetime_str(create_time)
        each_item = self._helper.build_answer(question, create_time, author, url, url, rank, content, self.domain)
        return each_item


    def _build_author(self, section, xpath_str):
        author = ''
        author_section = section.xpath(xpath_str).extract()
        if len(author_section) > 0:
            author = author_section[0]
        return author







