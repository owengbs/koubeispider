#!/usr/bin/python
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import hashlib
from hbase import Hbase
from hbase.ttypes import *
from thrift.transport import TSocket
from utils.config_utils import ConfigHelper

class ScrapydemoPipeline(object):
    hbase_info = ConfigHelper.get_hbase_info()

    def __init__(self):
        tsocket = TSocket.TSocket(self.hbase_info[0], self.hbase_info[1])
        self.transport = TTransport.TBufferedTransport(tsocket)
        protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
        self.client = Hbase.Client(protocol)
        self.transport.open()
        self.table_name = self.hbase_info[2]

    def __del__(self):
        self.transport.close()

    def process_item(self, item, spider):
        self.insert_data(item)
        return item

    def insert_data(self, item):
        author = Mutation(column="attributes:author", value=item['author'])
        create_time = Mutation(column="attributes:create_time", value=item['create_time'])
        from_url = Mutation(column="attributes:from_url", value=item['from_url'])
        post_url = Mutation(column="attributes:post_url", value=item['post_url'])
        rank = Mutation(column="attributes:rank", value=item['rank'])
        title = Mutation(column="attributes:title", value=item['title'])
        content_type = Mutation(column="attributes:content_type", value=item['content_type'])
        is_best = Mutation(column="attributes:is_best", value=item['is_best'])

        content = Mutation(column="content:", value=item['content'])
        mutations = [author, create_time, from_url, post_url, rank, title, content_type, is_best, content]
        rowKey = self.create_rowkey(item['domain'], item['post_url'],
                                    item['author'], item['create_time'], item['rank'])
        self.client.mutateRow(self.table_name, rowKey, mutations, None)


    # 渠道ID：4位（给每个网站一个编号）
    # URL md5：32位
    # 作者+时间+楼层 md5: 32位

    def create_rowkey(self, domain, post_url, author, create_time, rank):
        domain_id = ConfigHelper.get_domain_id(domain)
        m2 = hashlib.md5()
        m2.update(post_url)
        post_url_digest = m2.hexdigest()
        m2.update(author + create_time + rank)
        info_digest = m2.hexdigest()
        return domain_id + post_url_digest + info_digest


