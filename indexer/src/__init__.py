# -*- coding:utf-8 -*-
# coreseek3.2 python source
# author: xinyuan
# date: 2016-04-03 11:46
import os,sys, time
sys.path.append("../")
import apiservice.model.KoubeiLoader as KoubeiLoader
import apiservice.model.Question as Question
import logging
import redis
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='/Users/xinyuan/git/koubeispider/indexer/log/indexer.log',
                    filemode='w')

docid_rediskey_format = "coreseek_docid_%d"
def formatdate(x):
    format = "0000-00-00 00:00:00"
    if len(format) > len(x):
        x=x+format[len(x):]
    return x
class MainSource(object):
    def __init__(self, conf):
        self.conf =  conf
        self.idx = 0
        self.questionidx = 0
        self.loader = KoubeiLoader.KoubeiLoader()
        self.rediscli = redis.StrictRedis(host='127.0.0.1', port=6379) 
    def GetScheme(self):  #获取结构，docid、文本、整数
        return [
            ('id' , {'docid':True, } ),
            ('hbasedocid', {'type':'text'} ),
            ('title', { 'type':'text'} ),
            ('content', { 'type':'text'} ),
            ('create_time', {'type':'integer'} ),
        ]

    def GetFieldOrder(self): #字段的优先顺序
        return [('content', 'docid', 'title','create_time')]

    def Connected(self):   #如果是数据库，则在此处做数据库连接
        pass

    def NextDocument(self):   #取得每一个文档记录的调用
        logging.warn("self idx=%d" % (self.idx))
        (quests, self.questionidx) = self.loader.findQuestionByRank(self.questionidx)
        if len(quests) and quests[0]:
            quest = quests[0]
            self.id = self.idx+1
            self.title = ''
            self.hbasedocid = quest.docid
            self.content = quest.content
            timestr = formatdate(quest.createtime)
            print timestr
            self.create_time = int(time.mktime(time.strptime(timestr, "%Y-%m-%d %H:%M:%S")))
            self.rediscli.set(docid_rediskey_format % (self.id), self.hbasedocid)
            logging.warn("idx:%d hbasedocid:%s rediskey:%s content:%s" % (self.idx, self.hbasedocid, docid_rediskey_format % (self.id), self.content))
            self.idx += 1
            return True
        else:
            logging.warn("load finished idx:%d" % (self.idx))
            return False

if __name__ == "__main__":    #直接访问演示部分
    conf = {}
    source = MainSource(conf)
    source.Connected()
    logging.warn("hello connected")
    while source.NextDocument():
        print "id=%d, subject=%s" % (source.docid, source.subject)
    pass
#eof
