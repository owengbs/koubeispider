# -*- coding:utf-8 -*-
from scrapydemo.utils.item_helper import ItemHelper
from scrapydemo.ask_ci.url_helper import ParseHelper

class QzerParser(object):
    domain = "17qzer.com"

    def __init__(self):
        self._helper = ItemHelper()
        self._parse_helper = ParseHelper()

    def parse_page(self, response):
        items = list()
        title = response.xpath('//span[@id="thread_subject"]/text()')[0].extract()
        (is_first, post_url) = self.check_url(response.url)
        first_id = ''
        if is_first:
            items = self._parse_first_page(response, title)
        else:
            items = self._parse_answers(response, False, title, post_url)
        return items


    def _parse_first_page(self, response, title):
        items  = list()
        content = '';
        s = response.xpath('//a[@id="bbs_left"]/preceding-sibling::table[1]')
        se = s.xpath('//td[starts-with(@id, "postmessage_")]')[0]
        q = se.xpath('./text()').extract()
        for each in q:
            content = content + each
        section = response.xpath('//p[@class="ptn"]/span[@class="xi1"]/text()').extract()
        create_time = section[0]
        author = section[3]
        question_item = self._helper.build_question(title, create_time, author,
                                                    response.url, content,self.domain)

        items.append(question_item)

        answers = self._parse_answers(response, True, title, response.url)
        items = items + answers
        return items



    def _parse_answers(self, response, is_first, title, post_url):
        answers = list()
        msg_xpath = '//div[@id="postlist"]/div[starts-with(@id, "post_")]/@id'
        if is_first:
            msg_xpath = '//div[@id="postlist"]/div[starts-with(@id, "post_") and position()>1]/@id'
        m = response.xpath(msg_xpath)
        for each_m in m:
            id_str = each_m.extract().encode('utf-8')
            id = id_str.split('_')[1]
            time_xpath = '//em[@id="authorposton%s"]/text()' %id
            author_xpath = '//table[@id="pid%s"]/tr[1]/td[2]/div[1]/div/div[2]/a[2]/text()' %id
            answer_xpath = '//td[@id="postmessage_%s"]/descendant-or-self::*/text()' %id

            time = response.xpath(time_xpath).extract()[0]
            author = response.xpath(author_xpath).extract()[0]
            answer_section = response.xpath(answer_xpath)
            answer = ''
            for each in answer_section:
                answer = answer + each.extract()

            rank = self._get_rank(response, id)
            each = self._helper.build_answer(title, time, author, response.url, post_url,
                                      rank, answer, self.domain)
            answers.append(each)
        return answers





# http://www.17qzer.com/thread-139935-2-1.html
    def check_url(self, url):
        flag = True

        array = url.split('-')

        if array[2] == '1':
            pass
        else:
            flag = False
            array[2] = '1'
            url = '-'.join(array)
        return flag, url



    def _get_rank(self, response, id):
        rank_xpath = '//table[@id="pid%s"]/tr[1]/td[2]/div[1]/div/strong/a' % (id)
        rank_section = response.selector.xpath(rank_xpath)
        em = rank_section.xpath('./em/text()')
        if len(em) > 0:
            rank = em[0].extract().strip()
        else:
            rank = rank_section.xpath('./text()')[0].extract().strip()
        rank = rank.encode('utf-8')
        # if rank == '推荐':
        #      rank = '0'
        # elif rank == '楼主':
        #     rank = '1'
        if rank == '沙发':
            rank = '2'
        elif rank == '板凳':
            rank = '3'
        elif rank == '地板':
            rank = '4'
        return rank
