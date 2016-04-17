# -*- coding: utf-8 -*-
#
# $Id: conf.py 2055 2016-04-06 23:09:58Z xinyuan $
#
from sphinxapi import *
redis_host = '127.0.0.1'
redis_port = 6379

sphinx_host = 'localhost'
sphinx_port = 9312

dict_path = '/usr/local/mmseg/etc/'
docid_rediskey_format = "coreseek_docid_%d"
q = '看深秋'
mode = SPH_MATCH_EXTENDED2
rankmode = SPH_RANK_BM25
index = '*'
filtercol = 'group_id'
filtervals = []
sortby = 'create_time'
groupby = ''
groupsort = '@group desc'
limit = 100000
outputlimit = 5