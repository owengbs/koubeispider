import time

from scrapydemo.items import ScrapydemoItem


class MamaParser(object):

    domain="http://www.mama.cn"

    def parse_page(self, response):
        items = list()
        init_url = response.url
        if init_url.find('-p1.html') >0:
            question_best_items = self.parse_question_section(response)
            items = items + question_best_items
        more_answers = self.parse_more_answers(response)
        items = items + more_answers
        return items


    def parse_question_section(self, response):
        lists = list()
        s = response.selector.xpath("//section[@class='qaMain']/div[@class='qaCon cl']")
        author = ""
        author_section = s[0].xpath("./div[@class='user']/p[@class='name']/a/text()")
        if len(author_section)>0:
            author = author_section[0].extract()[0]
        title = self.get_title(response)




        create_time_str =response.selector.xpath("//p[@id='ask_info']/span[last()-1]/text()").extract()[0]      # create time
        create_time = self.handle_create_time(create_time_str)
        question_item = self.build_item(title, create_time, author, response.url, response.url, "", "0",title, "0", self.domain )
        lists.append(question_item)
        if len(s) == 2:
            author_best = ""
            author_best_section = s[1].xpath("./div[@class='user']/p[@class='name']/a/text()")  # author
            if len(author_best_section) ==1:
                author_best = author_best_section[0].extract()

            content_best = ""
            content_best_section = s[1].xpath("./div[@class='content']/div[@class='main']/descendant-or-self::*/text()")  #content
            for each  in content_best_section:
                content_best = content_best + each.extract()
            create_time_best_arrays = s[1].xpath("./div[@class='content']/p[@class='num']/span/text()").extract()# create_time
            create_time_best_str =  self.handle_createtime_section(create_time_best_arrays)
            create_time_best = self.handle_create_time(create_time_best_str)
            best_item = self.build_item(title, create_time_best, author_best, response.url, response.url, "", "1", content_best, "1", self.domain)
            lists.append(best_item)
        return lists



    def parse_more_answers(self, response):
        lists = list()
        title = self.get_title(response)
        qaCons = response.selector.xpath("//ul[@class='qaAllList']/li/div[@class='qaCon cl']")
        for qaCon  in qaCons:
            author = qaCon.xpath("./div[@class='user']/p[@class='name']/text()").extract()[0]
            contents = qaCon.xpath("./div[@class='content']/div[@class='main']/descendant-or-self::*/text()")
            content = ''
            for each in contents:
                content = content + each.extract()
            create_time_arrays = qaCon.xpath("./div[@class='content']/descendant-or-self::*/p[@class='num']/span/text()").extract()
            create_time_str =  self.handle_createtime_section(create_time_arrays)
            create_time = self.handle_create_time(create_time_str)
            post_url = self.build_post_url(response.url)
            answer_item = self.build_item(title, create_time, author, response.url, post_url,"", "1", content,"0", self.domain)
            lists.append(answer_item)
        return lists

    def  handle_createtime_section(self, create_time_arrays):
        create_time_str = ""
        if len(create_time_arrays) == 2:
            create_time_str = create_time_arrays[1]
        else:
            create_time_str = create_time_arrays[0]
        return create_time_str


    def get_title(self, response):
        title = ""
        title_section = response.selector.xpath("//h1[@id='ask_title']/text()").extract()  # title_section
        if len(title_section) == 1:
            title = title_section[0]
        return title



    def handle_create_time(self, create_time):
        index = create_time.find(' ')
        create_time = create_time[index:].strip()
        index_sub = create_time.find('-')
        if index_sub==2:
            create_time = str(time.localtime().tm_year) +"-" + create_time
        return create_time

    def build_post_url(self, from_url):
        p_index = from_url.find('-p')
        post_url = from_url[:p_index+2] + "1.html"
        return post_url

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

