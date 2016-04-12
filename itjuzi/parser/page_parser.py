# -*- coding:utf-8 -*-
from db_handler.mysql_handler import DBHelper
from db_info.funders_model import *
from utils.parser_utils import ParserUtils

class FunderParser():
    _phase_dict = dict()
    _industry_dict = dict()

    def __init__(self):
        self.db_helper = DBHelper()
        #self.db_helper.init_clean_data()
        self.session = self.db_helper.get_session()

        self._get_general_info()

#
    def _get_general_info(self):
        home_url = 'https://www.itjuzi.com/investevents'
        tree = ParserUtils.build_page_tree(home_url)

        infos = tree.xpath("/html/body/div[2]/div[1]/div[2]/div[1]/div[2]/ul")
        phase_list = self._parse_phase_info(infos)
        industry_list = self._parse_industry_info(infos)
        lists = phase_list + industry_list
        if self.db_helper.is_first_crawl():
            self.db_helper.insert_data(lists)
        self._build_dict(lists)
        print self._phase_dict
        print self._industry_dict


    def _build_dict(self, lists):
        for each in lists:
            print each.name
            if isinstance(each, FuPhase):
                self._phase_dict[each.name] = each.phaseid
            elif isinstance(each, FuIndustry):
                self._industry_dict[each.name] = each.pid
            else:
                print 'error data type '
                break


    # A 轮 B 轮
    def _parse_phase_info(self, infos):
        lists = list()
        dic_key = 'round'
        phase_section = infos[0].xpath('./li[2]/div/a')
        for each in phase_section:
            link = str(each.xpath("./@href")[0])
            value = ParserUtils.get_url_parameter(link, dic_key)
            if value is None:
                continue
            desc = each.xpath("./text()")[0].encode('utf-8').strip()
            new_phase = FuPhase(phaseid=int(value), name=desc)
            lists.append(new_phase)
        # add  并购
        new_phase = FuPhase(phaseid=20, name='并购')
        lists.append(new_phase)
        return lists

    # industry info

    def _parse_industry_info(self, infos):
        lists = list()
        dic_key = 'scope'
        phase_section = infos[0].xpath('./li[1]/div/a')
        for each in phase_section:
            link = str(each.xpath("./@href")[0])
            value = ParserUtils.get_url_parameter(link, dic_key)
            if value is None:
                continue
            desc = each.xpath("./text()")[0].encode('utf-8').strip()
            new_item = FuIndustry(pid=int(value), name=desc)
            lists.append(new_item)
        return lists



    def query_page_max(self):
        home_url = 'https://www.itjuzi.com/investfirm'
        tree = ParserUtils.build_page_tree(home_url)
        pagings = tree.xpath('//div[@class="ui-pagechange for-sec-bottom"]/a/@href')
        for each_page_link in pagings:
            if each_page_link == '':
                continue
            page_num = ParserUtils.get_url_parameter(str(each_page_link), 'page')
            max = 1
            if max < int(page_num):
                max = int(page_num)
        return max

    # parse detail page
    def parse_detail_page(self, req_url):
        lists = list()
        tree = ParserUtils.build_page_tree(req_url)  # etree.HTML(page)
        institution_name = tree.xpath('/html/body/div[2]/div[1]/div[2]/div/div[2]/p[1]/span[@class="title"]/text()')[0]
        institution_desc = tree.xpath('/html/body/div[2]/div[2]/div[2]/div[1]/div[2]/div[@class="des"]/text()')[0]
        institution_name = institution_name.encode('utf-8').strip()
        institution_desc = institution_desc.encode('utf-8').strip()

        FuInstitution(name=institution_name, describe=institution_desc)
        self.session.add(FuInstitution(name=institution_name, describe=institution_desc))
        self.session.commit()

        institution_id = self.session.query(FuInstitution).filter(FuInstitution.name == institution_name).first().id

        # invst_scopes
        invst_scope_xpath = '/html/body/div[2]/div[2]/div[2]/div[2]/div[2]/div/div/a'
        invst_scopes = self.parse_section('invst_scope', invst_scope_xpath, tree)

        # invst_state
        invst_state_xpath = '/html/body/div[2]/div[2]/div[2]/div[2]/div[4]/div/div/a'
        invst_states = self.parse_section('invst_state', invst_state_xpath, tree)

        print 'scopes: ', invst_scopes
        print 'states, ', invst_states

        # fu section
        fu_cases = tree.xpath('//table[@class="list-invecase limited-itemnum haslogin needfilter"]/tr')
        for each in fu_cases:
            fu_time = each.xpath('./td[1]/span/text()')[0].strip()
            fu_name = each.xpath('./td[3]/a/b/text()')[0].encode('utf-8').strip()
            fu_industry = each.xpath('./td[4]/span/text()')[0].encode('utf-8').strip()
            fu_phase = each.xpath('./td[5]/span/text()')[0].encode('utf-8').strip()
            fu_amount = each.xpath('./td[6]/span/text()')[0].encode('utf-8').strip()
            print fu_time, fu_name, fu_industry, fu_phase, fu_amount, institution_id
            case_item = self.insert_case_data(fu_time, fu_name, fu_industry, fu_phase, fu_amount, institution_id)
            lists.append(case_item)
        self.db_helper.insert_data(lists)



    def insert_case_data(self,fu_time, company_name, industry_name, phase_name, amount_message, institution_id):
        print phase_name

        if phase_name.startswith('并购'):
            phase_name = '并购'

        if industry_name.endswith('社交网络'):
            industry_name = '社交网络'
        elif industry_name.startswith('文化娱乐'):
            industry_name = '文化娱乐'
        phase_id = self._phase_dict[phase_name]
        company_id = self.query_company_id(company_name, industry_name)
        try:

            case_datetime = datetime.datetime.strptime(fu_time, "%Y.%m.%d")
        except:
            case_datetime = datetime.datetime.strptime("2017.1.1", "%Y.%m.%d")
        amount = 0
        return FuCase(phaseid=phase_id, companyid=company_id,
                      date=case_datetime, amount = amount,
                      amountmsg = amount_message, institutionid=institution_id,
                      comment='', author = '')


    def query_company_id(self, company_name, industry_name):
        result_company = self.session.query(FuCompany).filter(FuCompany.name == company_name).first()
        if result_company:
            company_id = result_company.id
        else:
            new_company = FuCompany(name=company_name, industryid=self._industry_dict[industry_name])
            self.session.add(new_company)
            company = self.session.query(FuCompany).filter(FuCompany.name == company_name).first()
            company_id = company.id
        return company_id



    def parse_section(self, dic_key, xpath_str, tree):
        id_list = list()
        link_sections = tree.xpath(xpath_str)
        for each_section in link_sections:
            link = each_section.xpath('./@href')[0]
            link = str(link)
            key_value = ParserUtils.get_url_parameter(link, dic_key)
            id_list.append(key_value)
        return id_list

if __name__ == "__main__":
    req_url = 'https://www.itjuzi.com/investfirm/2608'
    parser = FunderParser()
    parser.get_general_info()
    print parser.parse_detail_page(req_url)
    print 'end ...'