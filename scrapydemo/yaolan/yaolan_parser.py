
import urllib2
import urllib
from scrapydemo.items import ScrapydemoItem
from lxml import etree
import json


class YaolanParser(object):
    domain="ask.yaolan.com"

    def parse_page(self, response):
        items = list()
        question_item = self.parse_question_section(response)
        best_item = self.parse_best_answer(response, question_item['title'])
        more_answers = self.parse_more_answers(response, question_item['title'])
        items = list()
        items.append(question_item)
        items.append(best_item)
        items = items + more_answers
        return  items


    def parse_question_section(self, response):
        ext = response.selector.xpath("//div[@class='q_ask_con p_br']/h1/span/text()")
        title = ext[0].extract()
        ext = response.selector.xpath("//div[@class='q_ask_con p_br']/div[@class='in_sub']/span")
        author_section = ext[0].xpath('./a/text()').extract()
        author = ""
        if len(author_section)>0:
            author = author_section[0]
        create_time = ext[3].xpath("./text()").extract()[0]
        return self.build_item(title, create_time, author, response.url, response.url, "", "0",title, "0", self.domain )

    def parse_best_answer(self,response, title):
        create_time =response.selector.xpath("//div[@class='best_answer']/div[@class='padding20 clear']/span[@class='right time']/text()").extract()[0]
        content = response.selector.xpath("//div[@class='best_answer']/div[@class='cont']/text()").extract()[0]
        author = response.selector.xpath("//div[@class='best_answer']/div[@class='expert clear']/div[@class='bar']/p/a/text()").extract()[0]

        return self.build_item(title, create_time, author, response.url, response.url, "", "1", content, "1", self.domain)

    def parse_more_answers(self, response, title):
        answers = list()
        mores = response.selector.xpath("//div[@id='moreQuestion']/div[@class='expert_box']")
        for each in mores:
            author = each.xpath("./div[@class='clear']/div[@class='expert_a']/div[@class='bar']/a/text()").extract()[0]
            content = each.xpath("./div[@class='clear']/div[@class='expert_a']/p/text()").extract()[0]
            create_time = each.xpath("./div[@class='clear']/div[@class='expert_a']/div[@class='bar']/div[@class='r80']/text()").extract()[0]
            answer_item = self.build_item(title, create_time, author, response.url, response.url,"", "1", content,"0", self.domain)
            answers.append(answer_item)

        get_more = response.xpath("//div[@class='box_more']/a[@id='getmore']")
        if len(get_more)>0:
            ajax_items = self.parse_ajax_page(response, title)
            answers =answers + ajax_items
        return answers




    def  parse_ajax_page(self,response, title):
        lists = list()
        sel = response.selector.xpath("//input[@id='qid']/@value")
        qid = sel.extract()[0]
        req_url = "http://ask.yaolan.com/ajax/getMoreComment"
        data = {'qid':qid,'pagenum':'2'}
        data = urllib.urlencode(data)
        req = urllib2.Request(req_url, data)
        res = urllib2.urlopen(req)
        the_page = res.read()
        the_page_json = json.loads(the_page)
        tree = etree.HTML(the_page_json["msg"])
        nodes = tree.xpath("//div[@class='expert_box']/div[@class='clear']/div[@class='expert_a']")
        for node in nodes:
            author = node.xpath("./div[@class='bar']/a[1]/text()")[0]
            content = node.xpath("./p/text()")[0]
            create_time = node.xpath("./div[@class='bar']/div[@class='r80']/text()")[0]
            answer_item = self.build_item(title, create_time, author, response.url, response.url,"", "1", content,"0", self.domain)
            lists.append(answer_item)
        return lists


    def  build_item(self,title, create_time, author, from_url, post_url, rank, content_type, content, is_best,domain):
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



