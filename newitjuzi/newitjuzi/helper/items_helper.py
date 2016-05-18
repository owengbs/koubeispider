import calendar
from datetime import datetime

import re

from newitjuzi.db_handler.mysql_handler import DBHelper
from newitjuzi.helper.amount_helper import AmountHelper
from newitjuzi.models.funders_model import *



class ItemHelper():
    db_helper = DBHelper()


    @classmethod
    def insert_investevent(cls, time, companyName, type, phaseId, amountmsg, investorDict, comment, industryId, areaId):
        lists = list()
        time  = cls._handle_datetime(time.strip())
        companyName = cls._handle_value(companyName.strip())
        companyId = cls.query_company_id(companyName, industryId, areaId)
        type = type
        phaseId =phaseId
        print 'amountmsg :', amountmsg
        amountmsg = cls._handle_value(amountmsg)
        print 'amountmsg :', amountmsg
        amount, symbol_key = AmountHelper.convertAmount(amountmsg)
        comment = cls._handle_value(comment)
        for key in investorDict:
            value = investorDict[key]
            each = FuInvestEvent(phaseid=phaseId, companyid=companyId,
                                 date=time, amount=amount, amountmsg=amountmsg,
                                 symbol=symbol_key,institutionid=value, institutionmsg=key,
                                 comment=comment, author='', type=type)
            lists.append(each)
        cls.db_helper.insert_data(lists);

    @classmethod
    def insert_merger(cls, time, companyName, type, proportionmsg, amountmsg, investorDict, comment, industryId,
                           areaId):
        lists = list()
        time = cls._handle_datetime(time)
        companyName = cls._handle_value(companyName)
        companyId = cls.query_company_id(companyName, industryId, areaId)
        type = type
        print 'amountmsg :', amountmsg
        amountmsg = cls._handle_value(amountmsg)
        print 'amountmsg :', amountmsg

        amount, symbol_key = AmountHelper.convertAmount(amountmsg)
        proportionmsg = cls._handle_value(proportionmsg)
        proportion = cls._handle_proportion(proportionmsg)
        comment = cls._handle_value(comment)
        for key in investorDict:
            value = investorDict[key]
            each = FuMerger( companyid=companyId,
                            date=time, proportion=proportion,
                            proportionmsg=proportionmsg, amountmsg=amountmsg, amount=amount,symbol=symbol_key,
                            institutionid=value, institutionmsg=key,
                            comment=comment, author='', type=type)
            lists.append(each)
        cls.db_helper.insert_data(lists);

    @classmethod
    def insert_institution(cls, institutionId, name, description):
        institution = FuInstitution(institutionId=institutionId, name=name,
                                    describe=description)

        cls.db_helper.get_session().add(institution)
        cls.db_helper.get_session().commit()

    @classmethod
    def query_company_id(cls, company_name, industryId, areaId):
        if industryId is None:
            industryId = -1
        session = cls.db_helper.get_session()
        result_company = session.query(FuCompany).filter(FuCompany.name == company_name).first()
        if result_company:
            company_id = result_company.id
        else:
            new_company = FuCompany(name=company_name, industryid=industryId, areaid=areaId)
            session.add(new_company)
            company = session.query(FuCompany).filter(FuCompany.name == company_name).first()
            company_id = company.id
        return company_id


    @classmethod
    def _handle_proportion(cls, proportionmsg):
        pattern_1 = re.compile(r"^(\d+?)%$")
        matchs = pattern_1.match(proportionmsg)
        if matchs:
            return matchs.groups()[0]
        else:
            return -1

    @classmethod
    def _handle_value(cls, value):
        if isinstance(value, unicode):
            value = value.strip().encode('utf-8')
        return value.strip()

    @classmethod
    def _handle_datetime(cls, value):
        pattern_1 = re.compile(r"^(\d+?)\.(\d+?)\.(\d+?)$")
        pattern_2 = re.compile(r"^(\d+?)\.(\d+?)$")
        matchs = pattern_1.match(value)
        if matchs:
            try:
                dt = datetime.datetime(int(matchs.groups()[0]), int(matchs.groups()[1]), int(matchs.groups()[2]))
            except ValueError:
                print 'error datetime: ', value
                _, monthdays = calendar.monthrange(int(matchs.groups()[0]), int(matchs.groups()[1]))
                dt = datetime.datetime(int(matchs.groups()[0]), int(matchs.groups()[1]), monthdays)
            return dt

        matchs_2 = pattern_2.match(value)
        if matchs_2:
            return datetime.datetime(int(matchs_2.groups()[0]), int(matchs_2.groups()[1]), 1)


if __name__ == "__main__":
    value ='2016.4.27'
    print ItemHelper._handle_datetime(value)

