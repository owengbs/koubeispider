# -*- coding: utf-8 -*-
from newitjuzi.db_handler.mysql_handler import DBHelper
from newitjuzi.models.funders_model import FuInstitution


class NewitjuziPipeline(object):

    def __init__(self):
        self.db_helper = DBHelper()
        self.session = self.db_helper.get_session()

    def process_item(self, item, spider):

        return item



