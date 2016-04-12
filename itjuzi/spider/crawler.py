# -*- coding:utf-8 -*-
import random
import urllib
import urllib2

import time

from db_handler.mysql_handler import DBHelper
from parser.page_parser import FunderParser
from spider_filter.dupfilter import DupeFilter
from utils.parser_utils import ParserUtils


class itClawer():
    def __init__(self):
        self._data = {'identity': 'chenshao0594@126.com',
                       'password': 'Shaoqing@0594'
                       }
        db_helper = DBHelper()
        #db_helper.init_clean_data()
        self.parser = FunderParser()
        self.filter = DupeFilter()


    def crawling(self):
        page_number_max = self.parser.query_page_max()
        page_index = 99
        while (page_index <= page_number_max):
            paging_url = 'https://www.itjuzi.com/investfirm?page=%d'%(page_index)
            page_urls = self.parse_paging_page(paging_url)
            for ulr_detail in page_urls:
                if self.filter.request_seen(ulr_detail):
                    continue
                self.parser.parse_detail_page(ulr_detail)
                self.filter.insert_url(ulr_detail)
                time.sleep(random.uniform(0, 3))
            page_index = page_index +1

    # login to get cookie
    def login(self):
        login_url = 'https://www.itjuzi.com/user/login'
        post_data = urllib.urlencode(self._data)
        headers = {"User-agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1"}
        req = urllib2.Request(login_url, post_data, headers)
        self.opener.open(req)


    def parse_paging_page(self, paging_url):
        urls = list()
        tree = ParserUtils.build_page_tree(paging_url)
        nodes = tree.xpath("/html/body/div[2]/div[1]/div[2]/div[3]/div/div[1]/ul[2]/li")
        for each in nodes:
            urls.append(each.xpath("./i[1]/a/@href")[0])
        return urls

if __name__ == "__main__":
    req_url = 'https://www.itjuzi.com/investfirm/2608'
    crawler = itClawer()
    print crawler.crawling()
    print 'end ...'
