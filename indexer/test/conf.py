from sphinxapi import *
redis_host = '127.0.0.1'
redis_port = 6379

sphinx_host = 'localhost'
sphinx_port = 9312

docid_rediskey_format = "coreseek_docid_%d"
q = ''
mode = SPH_MATCH_ANY
index = '*'
filtercol = 'group_id'
filtervals = []
sortby = ''
groupby = ''
groupsort = '@group desc'
limit = 5