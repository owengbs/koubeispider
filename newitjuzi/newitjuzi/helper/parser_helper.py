# -*- coding:utf-8 -*-
import cookielib
import random
import urllib2
import urlparse

from lxml import etree

from newitjuzi.db_handler.mysql_handler import DBHelper
from newitjuzi.models.funders_model import FuIndustry, FuPhase, FuArea


class ParserHelper():
    scj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(scj))
    def __init__(self):
        self.db_helper = DBHelper()
        self.db_session = self.db_helper.get_session();

    def init_db(self):
        req_url = 'https://www.itjuzi.com/investevents'
        tree = self._build_page_tree(req_url)
        infos = tree.xpath('//ul[@class="ui-filterui"][1]')
        lists = list()
        lists = lists + self._parse_common_info(infos, 'scope')
        lists = lists+ self._parse_common_info(infos, 'prov')
        lists = lists + self._parse_common_info(infos, 'round')
        #https://www.itjuzi.com/investevents/foreign
        req_url = 'https://www.itjuzi.com/investevents/foreign'
        tree = self._build_page_tree(req_url)
        infos = tree.xpath('//ul[@class="ui-filterui"][1]')
        lists = lists + self._parse_common_info(infos, 'prov')
        self.db_helper.insert_data(lists)

    def _build_page_tree(self, req_url):
        ua = random.choice(self.user_agent_list)
        if ua:
            headers = {"User-agent": ua}
        req = urllib2.Request(url=req_url, data=None, headers=headers)
        page_result = self.opener.open(req)
        page = unicode(page_result.read(), "utf-8")
        page_tree = etree.HTML(page)
        return page_tree

    def _parse_common_info(self, infos, dic_key):
        lists = list()
        xpath_str='';
        if dic_key == 'scope':
            xpath_str = './li[1]/div/a'
        elif dic_key == 'round':
            xpath_str = './li[2]/div/a'
        elif dic_key == 'prov':
            xpath_str = './li[3]/div/a'
        phase_section = infos[0].xpath(xpath_str)
        for each in phase_section:
            link = str(each.xpath("./@href")[0])
            value = self.get_url_parameter(link, dic_key)
            if value is None:
                continue
            desc = each.xpath("./text()")[0].encode('utf-8').strip()
            if dic_key=='scope':
                new_item = FuIndustry(industryId=int(value), name=desc)
            elif dic_key=='round':
                new_item = FuPhase(phaseid=int(value), name=desc)
            elif dic_key =='prov':
                new_item = FuArea(name=desc);
            lists.append(new_item)
        return lists


    # to get parameter from url
    @classmethod
    def get_url_parameter(cls, req_url, key):
        if len(req_url)==0:
            return None
        result = urlparse.urlparse(req_url)
        qs_dict = urlparse.parse_qs(result.query, True)
        if qs_dict.has_key(key):
            return qs_dict[key][0]
        else:
            return None

    def get_area_dict(self):
        area_dict = dict()
        lists = self.db_session.query(FuArea).filter().all()
        for each in lists:
            area_dict[each.name.strip()] = each.id
        return area_dict

    def get_phase_dict(self):
        phase_dict = dict()
        lists = self.db_session.query(FuPhase).filter().all()
        for each in lists:
            phase_dict[each.name.strip()] = each.phaseid
        return phase_dict

    def get_industry_dict(self):
        phase_dict = dict()
        lists = self.db_session.query(FuIndustry).filter().all()
        for each in lists:
            phase_dict[each.name.strip()] = each.industryId
        return phase_dict

    user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1",
        "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11",
        "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6",
        "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6",
        "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1",
        "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 ",
        "(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 ",
        "(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5"
    ]


if __name__ == "__main__":
    req_url = 'https://www.itjuzi.com/investevents'
    parser = ParserHelper()
    parser.init_db()
    parser.get_phase_dict()


