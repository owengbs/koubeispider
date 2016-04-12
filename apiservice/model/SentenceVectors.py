#!/usr/bin/python
# -*- coding: UTF-8 -*-
import numpy as np
from scipy import spatial
import re
modelfile = "./data/test.vectors.txt"
sentencefile = "./data/test.content.txt.seged"

wordvecordict = {}
doclist = []
docvectorlist = []

def getDocvecBySegedLine(segline = ""):
    segs = segline.split()
    docvecs = []
    matchcount = 0
    for word in segs:
        if wordvecordict.has_key(word):
            docvecs.append(np.array(wordvecordict[word]))
            matchcount += 1
#     print docvecs
    if matchcount:
        return np.sum(docvecs, axis=0)/float(matchcount)
    else:
        return None
def getNearestDoc(docvector):
    global docvectorlist
    minindex = 0
    minsim = spatial.distance.cosine(docvector, docvectorlist[0])
    for i in range(1, len(docvectorlist)):
#         print docvector
#         print docvectorlist[i]
        try:
            simu = spatial.distance.cosine(docvector, docvectorlist[i])
            if simu < minsim:
                minsim = simu
                minindex = i
        except:
            print docvectorlist[i]
            exit(-1)
    return doclist[minindex]
"""
加载词向量
"""
loadmodellines = 0
for line in open(modelfile).readlines():
    segs = line.split()
    word = segs[0]
    wvector = [float(i) for i in segs[1:]]
    wordvecordict[word] = wvector
    loadmodellines += 1
    print "load %d model lines" % (loadmodellines)
    
"""
为每个句子生成句向量
"""
loaddoclines = 0
for line in open(sentencefile).readlines():
    docvector = getDocvecBySegedLine(line)
    if docvector is not None:
        doclist.append(line)
        docvectorlist.append(docvector)
        loaddoclines += 1
#     print docvectorlist
#     print "load %d doc lines" % (loaddoclines)
    
"""
接受输入,给出最相似的句子
"""
while True: 
    line = raw_input("please input a sentence")
    docvector = getDocvecBySegedLine(line)
    if docvector is not None:
        print getNearestDoc(docvector)
    else:
        print "word not in dict"