# -*- coding:utf-8 -*-
import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import *
from sqlalchemy import Column
Base = declarative_base()
# type: 0 not foreign
# type 1 foreign
#投资案例
class FuInvestEvent(Base):
    # name:
    __tablename__ = 'fu_investevent'
    # structure:
    id = Column(BigInteger, primary_key=True)
    type = Column(BigInteger)
    companyid = Column(BigInteger)
    phaseid = Column(BigInteger)
    institutionid = Column(BigInteger)
    institutionmsg = Column(String(128), default='')
    amount = Column(BigInteger)
    amountmsg = Column(String(128), default='')
    comment = Column(String(128))
    date = Column(DateTime, default=datetime.datetime.now())
    lastmodified = Column(DateTime, default=datetime.datetime.now())
    author = Column(VARCHAR(128), default='')


class FuMerger(Base):
    # name:
    __tablename__ = 'fu_merger'
    # structure:
    id = Column(BigInteger, primary_key=True)
    type = Column(BigInteger)
    companyid = Column(BigInteger)
    amount = Column(BigInteger)
    amountmsg = Column(String(128), default='')
    institutionid = Column(BigInteger)
    institutionmsg = Column(String(128), default='')
    proportion = Column(Float)
    proportionmsg = Column(String(128), default='')
    comment = Column(String(128))
    date = Column(DateTime, default=datetime.datetime.now())
    lastmodified = Column(DateTime, default=datetime.datetime.now())
    author = Column(VARCHAR(128), default='')


#企业描述
class FuCompany(Base):
    __tablename__ = 'fu_company'
    id = Column(BigInteger, primary_key=True)
    name = Column(VARCHAR(128))
    industryid = Column(BigInteger)
    areaid= Column(BigInteger)

#地区信息
class FuArea(Base):
    __tablename__ = 'fu_area'
    id = Column(BigInteger, primary_key=True)
    name = Column(VARCHAR(128))

##行业
class FuIndustry(Base):
    __tablename__ = 'fu_industry'
    id = Column(BigInteger, primary_key=True)
    pid = Column(BigInteger)
    industryId = Column(BigInteger)
    name = Column(VARCHAR(128))

#机构
class FuInstitution(Base):
    __tablename__ = 'fu_institution'

    id = Column(BigInteger, primary_key=True)
    institutionId = Column(BigInteger)
    name = Column(VARCHAR(128), default='')
    describe = Column(VARCHAR(128), default='')
    news = Column(VARCHAR(128), default='')
    lastmodified = Column(DateTime, default=datetime.datetime.now())
    author = Column(VARCHAR(128), default='')
#轮次
class FuPhase(Base):
    __tablename__ = 'fu_phase'
    id = Column(BigInteger, primary_key=True)
    phaseid = Column(BigInteger)
    name = Column(VARCHAR(128))
