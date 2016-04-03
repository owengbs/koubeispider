# -*- coding:utf-8 -*-

from scrapydemo.utils.itemhelper import ItemHelper
class MuYingParser(object):
    domain = "www.23myw.com"

    def parse_page(self, response):
        items = list()
        title = response.selector.xpath('//*[@id="thread_subject"]/text()')[0].extract()

        (is_first, post_url) = self.check_url(response)
        first_id = ''
        if is_first:
            first_id = response.selector.xpath('//*[@ id = "postlist"]/div[1]/@id').extract()[0].encode('utf-8')
        post_list = response.selector.xpath('//*[ @id = "postlist"]/div/@id')

        for each_post in post_list:
            id_str = each_post.extract().encode('utf-8')
            id_str_array = id_str.split('_')
            if len(id_str_array) == 1:
                continue
            id = id_str_array[1]

            author = self.get_anthor(response, id)

            content = self.get_content(response, id)

            create_time = self.get_create_time(response, id)
            rank = self.get_rank(response, id)
            helper = ItemHelper()
            if is_first and first_id == id_str:
                each = helper.build_question(title, create_time, author, response.url, content, self.domain)
            elif rank =='0':
                each = helper.build_best_answer(title, create_time, author, response.url, post_url, rank,
                                                content, self.domain)
            else:
                each = helper.build_answer(title, create_time, author, response.url, post_url, rank, content,
                                           self.domain)
            items.append(each)
        return items

    def check_url(self, response):
        flag = True
        if response.url.find('mod=viewthread') > 0:
            return flag, response.url
        s = response.url.split('-')
        if s[2] != '1':
            flag = False
            s[2] = '1'
        return flag, '-'.join(s)

    def get_anthor(self, response, id):
        author = ''
        author_xpath = '//*[@id="favatar%s"]/div[1]/div/a/text()' % (id)
        author_section = response.selector.xpath(author_xpath)
        if len(author_section)>0:
            author = author_section[0].extract()[0]
        return author


    def get_create_time(self, response, id):
        create_time_xpath = '//*[@id="authorposton%s"]/text()' % (id)
        create_time_str = response.selector.xpath(create_time_xpath).extract()[0]
        index = create_time_str.find(' ')
        return create_time_str[index:]

    def get_content(self, response, id ):
        content = ''
        content_xpath = '//*[@id="postmessage_%s"]/descendant-or-self::*/text()' % (id)
        content_sections = response.selector.xpath(content_xpath)
        for each in content_sections:
            content = content + each.extract()
        return content

    def get_rank(self, response, id):
        rank_xpath = '//*[@id="postnum%s"]' % (id)
        rank_section = response.selector.xpath(rank_xpath)
        em = rank_section.xpath('./em/text()')
        if len(em) > 0:
            rank = em[0].extract().strip()
        else:
            rank = rank_section.xpath('./text()')[0].extract().strip()
        rank = rank.encode('utf-8')
        if rank == '推荐':
            rank = '0'
        elif rank == '楼主':
            rank = '1'
        elif rank == '沙发':
            rank = '2'
        elif rank == '板凳':
            rank = '3'
        elif rank == '地板':
            rank = '4'
        return rank
