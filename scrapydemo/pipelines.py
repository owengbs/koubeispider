#coding:utf-8

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
	    	
    def process_item(self, item, spider):
        print '..... from_url ......'
        print item['post_url']
        print item['from_url']
        print item['create_time']
        print item['title']
        print ' ------ from url end -------'
        self.insert_data(item)

        return item


    def insert_data(self, item):
		author = Mutation(column="attributes:author", value=item['author'].encode('utf-8'))
		create_time = Mutation(column="attributes:create_time", value=item['create_time'])
		from_url=Mutation(column="attributes:from_url", value=item['from_url'].encode('utf-8'))
		post_url = Mutation(column="attributes:post_url", value=item['post_url'].encode('utf-8'))
		rank = Mutation(column="attributes:rank", value=item['rank'].encode('utf-8'))
		title=Mutation(column="attributes:title", value=item['title'].encode('utf-8'))
		content_type = Mutation(column="attributes:content_type", value=item['content_type'].encode('utf-8'))
		content = Mutation(column="content:", value=item['content'].encode('utf-8'))
		mutations = [author, create_time, from_url, post_url, rank,title, content_type, content,]
		rowKey= self.create_rowkey( item['author'].encode('utf-8') + item['create_time'].encode('utf-8') + item['rank'].encode('utf-8') )
		self.client.mutateRow('scrapydemo',rowKey , mutations, None)


    def create_rowkey(self, source):
        m2 = hashlib.md5()
        m2.update(source)
        return m2.hexdigest()

