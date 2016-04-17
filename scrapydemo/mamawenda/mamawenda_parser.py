# -*- coding:utf-8 -*-
from scrapydemo.utils.datetime_helper import DatetimeHelper
from scrapydemo.utils.item_helper import ItemHelper


class MamawendaParser(object):
    domain = "www.mamawenda.cn"


    def parse_page(self, response):
        helper = ItemHelper()
        url = response.url
        items = list()
        question = response.selector.xpath('//*[@id="conts_wrap"]/div[2]/div[1]/div/div[2]/div/text()')[0].extract()
        answer_section = response.selector.xpath('//*[@id="conts_wrap"]/div[2]/div[1]/div/div[3]/descendant-or-self::*/text()')
        create_time = self.build_create_time(response)
        question_item =helper.build_question(question, create_time, '', url, question, self.domain)
        if len(answer_section)>0:
            answer = ''
            for each in answer_section:
                answer = answer + each.extract()
            best_item = helper.build_best_answer(question, create_time, '', url, url, '1', answer, self.domain)
            items.append(best_item)
        items.append(question_item)
        return items



    def parse_wenda_page(self, response):
        wenda_items = list()
        question_item = self.build_question_item(response)
        answer_items = self.build_answer_items(response, question_item['title'])
        wenda_items.append(question_item)
        wenda_items = wenda_items + answer_items
        return wenda_items



    def build_create_time(self, response):
        create_time = response.selector.xpath('//*[@id="conts_wrap"]/div[2]/div[1]/div/div[1]/span[2]/text()[last()]').extract()[0]
        create_time = DatetimeHelper.build_datetime_str(create_time.strip())
        return create_time



    def build_question_item(self, response):
        helper = ItemHelper()
        author_section = response.selector.xpath('//*[@id="conts_wrap"]/div[2]/div[1]/ul[@class="q_list marRL"]/li/h2/text()')
        author = author_section.extract()[0]
        create_time_str =  response.selector.xpath('//*[@id="conts_wrap"]/div[2]/div[1]/ul[@class="q_list marRL"]/li/p[2]/text()').extract()[0]
        create_time = DatetimeHelper.build_datetime_str(create_time_str.strip())
        content_section =  response.selector.xpath('//*[@id="conts_wrap"]/div[2]/div[1]/div[@class="q_conts"]/descendant-or-self::*/text()')
        content = ''
        for each in content_section:
             content = content + each.extract()
        return helper.build_question(content, create_time, author, response.url, content, self.domain)

    def build_answer_items(self, response, title):
        req_url = response.url
        items = list()
        helper = ItemHelper()
        reply_list_xpath = '//*[@id ="conts_wrap"]/div[2]/div[1]/div[@class="reply_list"]/ul[@class="q_list"]/li'
        reply_section = response.selector.xpath(reply_list_xpath)
        rank = 1
        for each in reply_section:
            content = each.xpath('./p[@class="conts"]/text()').extract()[0]
            create_time_str = each.xpath('./p[@class="time"]/text()').extract()[0]
            create_time = DatetimeHelper.build_datetime_str(create_time_str)
            author = each.xpath('./h2/text()').extract()[0]
            each_item = helper.build_answer(title, create_time, author, req_url, req_url, str(rank), content, self.domain)
            items.append(each_item)
            rank = rank+1
        return items

