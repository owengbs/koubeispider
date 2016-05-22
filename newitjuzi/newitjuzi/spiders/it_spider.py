# -*- coding: utf-8 -*-
import urlparse

import scrapy
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.spiders import Rule, CrawlSpider

from newitjuzi.helper.items_helper import ItemHelper
from newitjuzi.helper.parser_helper import ParserHelper
from newitjuzi.items import InstitutionItem


class ITSpider(scrapy.Spider):
    name = "itjuzi"
    allowed_domains = ['itjuzi.com']
    _base_url = 'https://www.itjuzi.com'
    custom_settings = {'CONCURRENT_REQUESTS': 1,
                       'CONCURRENT_REQUESTS_PER_IP': 1,
                       'AUTOTHROTTLE_ENABLED': True,
                       'RETRY_TIMES': 10,
                       }

    _MERGER = 'merger'
    _MERGER_FOREIGN='merger/foreign'
    _INVESTEVENTS ='investevents'
    _INVESTEVENTS_FOREIGN='investevents/foreign'

    start_urls = [
        'https://www.itjuzi.com/investevents',
        'https://www.itjuzi.com/merger',
        'https://www.itjuzi.com/investevents/foreign',
        'https://www.itjuzi.com/merger/foreign',
    ]

    def __init__(self, *a, **kw):
        super(ITSpider, self).__init__(*a, **kw)
        parser_helper = ParserHelper()
        parser_helper.init_db()
        self.phase_dict = parser_helper.get_phase_dict()
        self.area_dict = parser_helper.get_area_dict()
        self.scope_dict = parser_helper.get_industry_dict()

    def parse(self, response):
        self.parse_paging_page(response)
        #
        for question_url in response.xpath('//i[@class="cell date"]/span[@class="investorset"]/a/@href').extract():
            question_url = urlparse.urljoin(self._base_url, question_url)
            yield scrapy.Request(question_url, callback=self._parse_institution)
        for investfirm_url in response.xpath('//i[@class="cell date"]/a/@href').extract():
            yield scrapy.Request(investfirm_url, callback=self._parse_institution)

        for url in response.xpath('//div[@class="ui-pagechange for-sec-bottom"]/a/@href').extract():
            url = urlparse.urljoin(self._base_url, url)
            yield scrapy.Request(url, callback=self.parse)




    def parse_paging_page(self, response):
        event_type = self._get_case_type(response.url)
        if event_type==self._MERGER_FOREIGN or event_type==self._MERGER:
            self._parse_merger(response,event_type)

        elif event_type==self._INVESTEVENTS or event_type==self._INVESTEVENTS_FOREIGN:
            self._parse_investevents(response,event_type)


    def _get_case_type(self, req_url):
        url = urlparse.urlparse(req_url)
        path_url = url.path
        if path_url.endswith(self._INVESTEVENTS):
            return self._INVESTEVENTS

        elif path_url.endswith(self._INVESTEVENTS_FOREIGN):
            return self._INVESTEVENTS_FOREIGN

        elif path_url.endswith(self._MERGER):
            return self._MERGER

        elif path_url.endswith(self._MERGER_FOREIGN):
            return self._MERGER_FOREIGN

    def _parse_institution(self, response):
        item = InstitutionItem()
        req_url = response.url
        index = req_url.rfind('/')
        institution_id = req_url[index + 1:]
        institution_name = response.selector.xpath('//div[@class="boxed rel"]/div[@class="picinfo"]/p/span[@class="title"]/text()').extract()[0]
        institution_desc = response.selector.xpath('//div[@class="des"]/text()').extract()[0]
        institution_name = institution_name.encode('utf-8').strip()
        institution_desc = institution_desc.encode('utf-8').strip()
        ItemHelper.insert_institution(institutionId=institution_id, name=institution_name,
                                      description=institution_desc)
        return item




    def _get_value(self, key, key_dict):
        key = key.strip()
        return key_dict[key]



    def _parse_merger(self, response, event_type):
        lis = response.selector.xpath('//ul[@class="list-main-eventset"]/li')
        for each in lis:
            time = each.xpath('./i[@class="cell round"]/span/text()').extract()[0]
            companyName = each.xpath('./p[@class="title"]/a/span/text()').extract()[0]
            # foreign
            scope_desc = each.xpath('./p/span[@class="tags t-small c-gray-aset"]/a/text()').extract()[0]
            scope_value = self.scope_dict[scope_desc]

            prov_name = each.xpath('./p/span[@class="loca c-gray-aset t-small"]/span/text()').extract()[0]
            prov_value = self._get_value(prov_name, self.area_dict)
            proportionmsg = each.xpath('./i[@class="cell round"]/span[@class="tag gray"]/text()').extract()[0].strip()
            if event_type == self._MERGER:
                type = 0
            else:
                type = 1

            # fina_msg : 数千万等
            amountmsg = each.xpath('./i[@class="cell fina"]//text()').extract()[0].strip()
            investor_dict = self._merger_investor_dict(each)
            ItemHelper.insert_merger(time=time, companyName=companyName, type=type, proportionmsg=proportionmsg,
                                     amountmsg=amountmsg, investorDict=investor_dict, comment='',
                                     industryId=scope_value, areaId=prov_value)


    def _parse_investevents(self, response, case_type):
        lis = response.selector.xpath('//ul[@class="list-main-eventset"]/li')
        for each in lis:
            time = each.xpath('./i[@class="cell round"]/span/text()').extract()[0]
            companyName = each.xpath('./p[@class="title"]/a/span/text()').extract()[0]
            # https://www.itjuzi.com/investevents?scope=70 => 社交网络 行业
            scope_sec = each.xpath('./p/span[@class="tags t-small c-gray-aset"]/a/@href').extract()
            if len(scope_sec)>0:
                scope_url = scope_sec[0]
            else:
                scope_url = ''

            scope_value = ParserHelper.get_url_parameter(scope_url, 'scope')

            if case_type==self._INVESTEVENTS:
                prov_name = each.xpath('./p/span[@class="loca c-gray-aset t-small"]/a/text()').extract()[0]
            else:
                prov_name = each.xpath('./p/span/span[@class="t-small"]/text()').extract()[0]
            prov_value = self._get_value(prov_name, self.area_dict)
            if case_type == self._INVESTEVENTS:
                phase_name = each.xpath('./i[@class="cell round"]/a/span[@class="tag gray"]/text()').extract()[0]
                type =0
            else:
                phase_name = each.xpath('./i[@class="cell round"]/span[@class="tag gray"]/text()').extract()[0]
                type =1
            phase_value = self._get_value(phase_name, self.phase_dict)

            # fina_msg : 数千万等
            amountmsg = each.xpath('./i[@class="cell fina"]//text()').extract()[0].strip()
            investor_dict = self._build_investor_dict(each)
            ItemHelper.insert_investevent(time=time, companyName=companyName, type=type, phaseId=phase_value,
                                          amountmsg=amountmsg, investorDict=investor_dict, comment='',
                                          industryId=scope_value, areaId=prov_value)

    def _build_investor_dict(self, element):
        investor_dict = dict()
        investorSet = element.xpath('./i[@class="cell date"]/span[@class="investorset"]/a')
        for each in investorSet:
            investfirm_url = each.xpath('./@href').extract()[0].encode('utf-8').strip()
            index = investfirm_url.rfind('/')
            investfirm_id = investfirm_url[index + 1:]
            investfirm_name = each.xpath('./text()').extract()[0].encode('utf-8').strip()
            investor_dict[investfirm_name] = investfirm_id
        investorSet_2 = element.xpath('./i[@class="cell date"]/span[@class="investorset"]/span[@class="c-gray"]/text()')
        for each in investorSet_2:
            name = each.extract().encode('utf-8').strip()
            investor_dict[name] = -1
        return investor_dict

    def _merger_investor_dict(self, element):
        investor_dict = dict()
        investorSet = element.xpath('./i[@class="cell date"]/a')
        for each in investorSet:
            investfirm_url = each.xpath('./@href').extract()[0].encode('utf-8').strip()
            index = investfirm_url.rfind('/')
            investfirm_id = investfirm_url[index + 1:]
            investfirm_name = each.xpath('./text()').extract()[0].encode('utf-8').strip()
            investor_dict[investfirm_name] = investfirm_id
        investorSet_2 = element.xpath('./i[@class="cell date"]/span[@class="c-gray"]/text()')
        for each in investorSet_2:
            name = each.extract().encode('utf-8').strip()
            investor_dict[name] = -1
        return investor_dict




















