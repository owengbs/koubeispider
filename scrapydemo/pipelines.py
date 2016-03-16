#!/usr/bin/python
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import random
import hashlib

from thrift.transport import TSocket

from hbase import Hbase
from hbase.ttypes import *



class ScrapydemoPipeline(object):

    def __init__(self):
		tsocket = TSocket.TSocket('localhost', 9090)
		transport = TTransport.TBufferedTransport(tsocket)
		protocol = TBinaryProtocol.TBinaryProtocol(transport)
		self.client = Hbase.Client(protocol)
		transport.open()
		self.table_name='demo'

    def process_item(self, item, spider):
		self.insert_data(item)
		return item


    def insert_data(self, item):
		author = Mutation(column="attributes:author", value=item['author'].strip().encode('utf-8'))
		create_time = Mutation(column="attributes:create_time", value=item['create_time'])
		from_url=Mutation(column="attributes:from_url", value=item['from_url'].encode('utf-8'))
		post_url = Mutation(column="attributes:post_url", value=item['post_url'].encode('utf-8'))
		rank = Mutation(column="attributes:rank", value=item['rank'].encode('utf-8'))
		title=Mutation(column="attributes:title", value=item['title'].strip().encode('utf-8'))
		content_type = Mutation(column="attributes:content_type", value=item['content_type'].encode('utf-8'))
		is_best = Mutation(column="attributes:is_best", value=item['is_best'])

		content = Mutation(column="content:", value=item['content'].strip().encode('utf-8'))
		mutations = [author, create_time, from_url, post_url, rank,title, content_type, is_best,content]
		rowKey= self.create_rowkey( item['domain'],item['post_url'].encode('utf-8'),
                                    item['author'].encode('utf-8'), item['create_time'].encode('utf-8'), item['rank'].encode('utf-8'))
		self.client.mutateRow(self.table_name,rowKey , mutations, None)

    #渠道ID：4位（给每个网站一个编号）
    #URL md5：32位
    #作者+时间+楼层 md5: 32位

    def create_rowkey(self, domain, post_url, author, create_time, rank):
        domain_id = self.domain_dict[domain]
        m2 = hashlib.md5()
        m2.update(post_url)
        post_url_digest = m2.hexdigest()
        m2.update(author+create_time+rank)
        info_digest = m2.hexdigest()
        print domain_id+post_url_digest+info_digest
        return domain_id+post_url_digest+info_digest

    domain_dict = {"www.babytree.com":"0001",
				   "ask.yaolan.com":"0002"}