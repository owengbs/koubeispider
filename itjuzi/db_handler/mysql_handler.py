# -*- coding:utf-8 -*-

from sqlalchemy import Column, create_engine
from sqlalchemy.orm import sessionmaker
from db_info.funders_model import *
from utils.config_utils import *



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

    def init_clean_data(self):
        self.session.query(FuPhase).delete()
        self.session.query(FuIndustry).delete()
        self.session.query(FuInstitution).delete()
        self.session.query(FuCase).delete()
        self.session.query(FuCompany).delete()

        self.session.commit()

    def insert_data(self, lists):
        for each in lists:
            self.session.add(each)
        self.session.commit()

    def is_first_crawl(self):
        if self.session.query(FuPhase).all():
            return False
        else:
            return True


if __name__ == '__main__':
    helper_1 = DBHelper()
    session_1 = helper_1.get_session()
    new_phase = FuPhase(name='天使56')
    session_1.add(new_phase)
    result = session_1.query(FuPhase).filter(FuPhase.name=='天使56').first()
    print result.id

    phase =  session_1.query(FuPhase).first()
    print phase.id
    print phase.name
    print phase.phaseid
    print '........'
    result = session_1.query(FuPhase).filter(FuPhase.name=='kijkjbu56').all()
    print len(result)
    if result:
        print 'empty ... '
    else :
        print 'not empty'
    print '....'
    session_1.query(FuPhase).delete()
    session_1.commit()
    session_1.close()





