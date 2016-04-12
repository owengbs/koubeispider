# -*- coding: utf-8 -*-
import hashlib
import Question
import HbaseBase
import PostItem
class KoubeiLoader(HbaseBase.HbaseBase):
    #code
    def __init__(self):
        HbaseBase.HbaseBase.__init__(self)
    def findQuestionWithAnsersByUrl(self, domainId, postUrl):
        question = Question.Question()
        m = hashlib.md5()
        m.update(postUrl)
        urlmd5 = m.hexdigest()
        all0_32 = "".join(['0' for i in range(32)])
        allf_32 = "".join(['f' for i in range(32)])
        start = domainId+urlmd5+all0_32
        end = domainId+urlmd5+allf_32
        # print "startrow:%s stoprow:%s" % (start, end)
        rows = self.scanByRange(start, end)
        for row in rows:
            docid = row[0]
            columns = row[1]
            title = columns["attributes:title"]
            createtime = columns["attributes:create_time"]
            from_url = columns["attributes:from_url"]
            post_url = columns["attributes:post_url"]
            author = columns["attributes:author"]
            rank = columns["attributes:rank"]
            content = columns["content:"]
            if columns["attributes:content_type"] == '0':
                question.setPostItem(docid, content, createtime, from_url, post_url, author, rank)
            else:
                postitem = PostItem.PostItem(docid, content, createtime, from_url, post_url, author, rank)
                question.answers.append(postitem)
        # print len(question.answers)
        return question
    def findQuestionByRank(self, index = 0):
        quests = []
        start = "".join(['0' for i in range(68)])
        end = "".join(['f' for i in range(68)])
        while len(quests) == 0:
            rows = self.scanRangeByRank(start, end, None, index, 1)
            if len(rows):
                question = Question.Question()
                for row in rows:
                    docid = row[0]
                    columns = row[1]
                    title = columns["attributes:title"]
                    createtime = columns["attributes:create_time"]
                    from_url = columns["attributes:from_url"]
                    post_url = columns["attributes:post_url"]
                    author = columns["attributes:author"]
                    rank = columns["attributes:rank"]
                    content = columns["content:"]
                    if columns["attributes:content_type"] == '0':
                        question.setPostItem(docid, content, createtime, from_url, post_url, author, rank)
                        quests.append(question)
            else:
                break
            index += 1
        return (quests, index)
    def findQuestionByDocid(self, docid = ''):
        question = Question.Question()
        columns = self.getRow(docid)
        title = columns["attributes:title"]
        createtime = columns["attributes:create_time"]
        from_url = columns["attributes:from_url"]
        post_url = columns["attributes:post_url"]
        author = columns["attributes:author"]
        rank = columns["attributes:rank"]
        content = columns["content:"]
        question.setPostItem(docid, content, createtime, from_url, post_url, author, rank)
        return question

if __name__ == '__main__':
    #http://ask.yaolan.com/question/15060221040878428934.html
    #http://ask.yaolan.com/question/15050520113034135325.html
    loader = KoubeiLoader()
    quest = loader.findQuestionWithAnsersByUrl("0003", "http://www.mama.cn/ask/q4911671-p1.html")
    print "【问题】docid:%s content:%s" % (quest.docid, quest.content)
    i = 1
    for each  in  quest.getAnswerContents():
        print ' ......'+str(i)+'......'
        print each
        i = i +1
    (quests , index) = loader.findQuestionByRank(0)
    print "【问题】docid:%s content:%s" % (quests[0].docid, quests[0].content)
    i = 1
    for each  in  quests[0].getAnswerContents():
        print ' ......'+str(i)+'......'
        print each
        i = i +1
    quest = loader.findQuestionByDocid("0003ae31d0dbcfc0060eb24740639c313e099e7a9a3141fdce41a10d84d0c0f2c79d")
    print "【问题】docid:%s content:%s" % (quest.docid, quest.content)
    quest_ans = loader.findQuestionWithAnsersByUrl(quest.docid[:4], quest.post_url)
    print  quest.docid[:4]
    i = 1
    for each  in  quest_ans.getAnswerContents():
        print ' ......'+str(i)+'......'
        print each
        i = i +1