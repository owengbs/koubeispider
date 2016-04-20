from scrapy import Selector

from scrapydemo.utils.item_helper import ItemHelper


class KuaiwenParser(object):
    domain = "kuaiwen.pcbaby.com.cn"

    def __init__(self):
        self.helper = ItemHelper()

    def parse_page(self, response):
        res_selector = Selector(response)
        url = response.url
        items = list()
        question_item = self._build_question(res_selector, url)
        title = question_item['title']
        items.append(question_item)
        best_item = self._build_best_answer(res_selector, title ,url)
        start_rank =1
        if best_item is not None:
            items.append(best_item)
            start_rank = 2
        answers = self._build_answers(res_selector, title, url, start_rank)
        items = items + answers
        return items

    def _build_question(self, res_selector, url):
        title_xpath = '//div[@class="wt-box mb30 part"]/dl/dd/p[@class="wt-PicTxt-Title"]'
        title = self._build_section(res_selector, title_xpath)
        author = res_selector.xpath('//div[@class="wt-box mb30 part"]/dl/dd/p[1]/span[1]/a/text()').extract()[0]
        create_time = res_selector.xpath('//div[@class="wt-box mb30 part"]/dl/dd/p[1]/span[2]/i[2]/text()').extract()[0]
        content_xpath = '//div[@class="wt-box mb30 part"]/dl/dd/p[@class="wt-PicTxt-Txt"]'
        content = self._build_section(res_selector, content_xpath)
        return self.helper.build_question(title, create_time, author, url,content, self.domain)


    def _build_best_answer(self, res_selector, title, url):
        best_section = res_selector.xpath('//*[@id="Jbody"]/div[6]/div[1]/div[1]/div/dl/dd')
        if len(best_section) ==0:
            return None

        author = best_section.xpath('./p/span[1]/i[1]/a/text()').extract()[0]
        create_time = best_section.xpath('./p/span[1]/i[2]/text()').extract()[0]
        content_xpath = './div[@class="wt-PicTxt-Txt"]'
        content = self._build_section(best_section, content_xpath)

        return self.helper.build_best_answer(self, title, create_time, author, url,
                                             url, '1', content, self.domain)



    def _build_answers(self, res_selector, title, url, init_rank):
        lists = list()
        answers_section = res_selector.xpath('//div[@class="lBox part mb30 wt-wd"]/div[@class="lBox-tb"]/dl/dd[@class="last"]')
        rank = init_rank
        for each in answers_section:
            author = each.xpath('./p/span[1]/i[1]/a/text()').extract()[0]
            create_time = each.xpath('./p/span[1]/i[last()]/text()').extract()[0]
            content_xpath = './div[@class="wt-PicTxt-Txt"]'
            content = self._build_section(res_selector, content_xpath)
            each_item = self.helper.build_answer(title, create_time, author, url, url, str(rank), content, self.domain)
            rank = init_rank +1
            lists.append(each_item)
        return lists

    def _build_section(self, res_selector, xpath):
        xpath = xpath + '/descendant-or-self::*/text()'
        content_section = res_selector.xpath(xpath)
        content = ''
        for each in content_section:
            content = content + each.extract()
        return content
