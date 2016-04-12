# -*- coding:utf-8 -*-
import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import *
from sqlalchemy import Column
Base = declarative_base()
class FuCase(Base):
    # name:
    __tablename__ = 'fu_case'

    # structure:
    id = Column(BigInteger, primary_key=True)
    companyid = Column(BigInteger)
    phaseid = Column(BigInteger)
    institutionid = Column(BigInteger)
    amount = Column(BigInteger)
    amountmsg = Column(String(128), default='')
    comment = Column(String(128))
    date = Column(DateTime, default=datetime.datetime.now())
    lastmodified = Column(DateTime, default=datetime.datetime.now())
    author = Column(VARCHAR(128))

class FuCompany(Base):
    __tablename__ = 'fu_company'

    id = Column(BigInteger, primary_key=True)
    name = Column(VARCHAR(128))
    industryid = Column(BigInteger)

class FuIndustry(Base):
    __tablename__ = 'fu_industry'

    id = Column(BigInteger, primary_key=True)
    pid = Column(BigInteger)
    name = Column(VARCHAR(128))


class FuInstitution(Base):
    __tablename__ = 'fu_institution'

    id = Column(BigInteger, primary_key=True)
    name = Column(VARCHAR(128), default='')
    describe = Column(VARCHAR(128), default='')
    news = Column(VARCHAR(128), default='')
    lastmodified = Column(DateTime, default=datetime.datetime.now())
    author = Column(VARCHAR(128), default='')


class FuPhase(Base):
    __tablename__ = 'fu_phase'
    id = Column(BigInteger, primary_key=True)
    phaseid = Column(BigInteger)
    name = Column(VARCHAR(128))

