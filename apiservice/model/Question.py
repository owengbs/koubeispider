# -*- coding: utf-8 -*-
import hashlib
import Answer
import HbaseBase
class Question(HbaseBase.HbaseBase):
    #code
    def __init__(self, domainId, postUrl= ""):
        self.answers = []
        self.titleid = 0
        HbaseBase.HbaseBase.__init__(self)
        m = hashlib.md5()
        m.update(postUrl)
        urlmd5 = m.hexdigest()
        all0_32 = "".join(['0' for i in range(32)])
        allf_32 = "".join(['f' for i in range(32)])
        start = domainId+urlmd5+all0_32
        end = domainId+urlmd5+allf_32
        rows = self.scanByRange(start, end)
        for row in rows:
            title = row["attributes:title"]
            createtime = row["attributes:create_time"]
            from_url = row["attributes:from_url"]
            post_url = row["attributes:post_url"]
            author = row["attributes:author"]
            rank = row["attributes:rank"]
            content = row["content:"]
            self.answers.append(Answer.Answer(content, createtime, from_url, post_url, author, rank))
            if row["attributes:content_type"] == '0':
                self.titleid = len(self.answers) - 1
    def getAnswerContents(self):
        return [self.answers[i].content for i in range(len(self.answers)) if i is not self.titleid]
    def getQuestionContent(self):
        return self.answers[self.titleid].content
if __name__ == '__main__':
    quest = Question("0001","http://www.babytree.com/ask/detail/24635111")
    print "【问题】:%s" % (quest.getQuestionContent())
    print "\n".join(quest.getAnswerContents())