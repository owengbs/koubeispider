# -*- coding: utf-8 -*-
import hashlib
import PostItem
import HbaseBase
class Question(PostItem.PostItem):
    #code
    def __init__(self):
        self.answers = []
    def setPostItem(self,
                    docid = "", content = "", createtime = "",
                    from_url = "", post_url = "", author = "", rank = 0):
        PostItem.PostItem.__init__(self, docid, content, createtime, from_url, post_url, author, rank)
    def getAnswerContents(self):
        return [self.answers[i].content for i in range(len(self.answers))]