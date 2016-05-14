# -*- coding:utf-8 -*-
from sqlalchemy import Column, create_engine
from sqlalchemy.orm import sessionmaker

from newitjuzi.models.funders_model import *
from newitjuzi.utils.config_utils import ConfigUtils


class DBHelper():
    def __init__(self):
        infos = ConfigUtils.get_db_info()
        engine_str = 'mysql+mysqlconnector://%s:%s@%s:%s/%s' % (infos[2], infos[3], infos[0], infos[1], infos[4])
        engine = create_engine(engine_str)
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()

    def get_session(self):
        return self.session

    def __del__(self):
        self.session.close()

    def insert_data(self, lists):
        print lists
        for each in lists:
            self.session.add(each)
        self.session.commit()