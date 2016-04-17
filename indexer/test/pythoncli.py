# -*- coding: utf-8 -*- 
#
# $Id: test.py 2055 2016-04-06 23:09:58Z xinyuan $
#

from sphinxapi import *
import cmmseg
import sys, time
sys.path.append("../")
import apiservice.model.HbaseBase as HbaseBase
import apiservice.model.KoubeiLoader as KoubeiLoader
import redis
import conf
rediscli = redis.StrictRedis(host=conf.redis_host, port=conf.redis_port)
hbasecli = HbaseBase.HbaseBase()
koubeicli = KoubeiLoader.KoubeiLoader()
cmmseg.init(conf.dict_path)
def Usage():
	print "Usage: python test.py [OPTIONS] query words\n"
	print "Options are:"
	print "-h, --host <HOST>\tconnect to searchd at host HOST"
	print "-p, --port\t\tconnect to searchd at port PORT"
	print "-i, --index <IDX>\tsearch through index(es) specified by IDX"
	print "-s, --sortby <EXPR>\tsort matches by 'EXPR'"
	print "-a, --any\t\tuse 'match any word' matching mode"
	print "-b, --boolean\t\tuse 'boolean query' matching mode"
	print "-e, --extended\t\tuse 'extended query' matching mode"
	print "-f, --filter <ATTR>\tfilter by attribute 'ATTR' (default is 'group_id')"
	print "-v, --value <VAL>\tadd VAL to allowed 'group_id' values list"
	print "-g, --groupby <EXPR>\tgroup matches by 'EXPR'"
	print "-gs,--groupsort <EXPR>\tsort groups by 'EXPR'"
	print "-l, --limit <COUNT>\tretrieve COUNT matches (default is 20)"
	sys.exit(0)


def formatdate(x):
    format = "0000-00-00 00:00:00"
    if len(format) > len(x):
        x=x+format[len(x):]
    return x
def parseparam():
	i = 1
	while (i<len(sys.argv)):
		arg = sys.argv[i]
		if arg=='-h' or arg=='--host':
			i += 1
			conf.sphinx_host = sys.argv[i]
		elif arg=='-p' or arg=='--port':
			i += 1
			conf.sphinx_port = int(sys.argv[i])
		elif arg=='-i':
			i += 1
			conf.index = sys.argv[i]
		elif arg=='-s':
			i += 1
			conf.sortby = sys.argv[i]
		elif arg=='-a' or arg=='--any':
			conf.mode = SPH_MATCH_ANY
		elif arg=='-b' or arg=='--boolean':
			conf.mode = SPH_MATCH_BOOLEAN
		elif arg=='-e' or arg=='--extended':
			conf.mode = SPH_MATCH_EXTENDED
		elif arg=='-f' or arg=='--filter':
			i += 1
			conf.filtercol = sys.argv[i]
		elif arg=='-v' or arg=='--value':
			i += 1
			conf.filtervals.append ( int(sys.argv[i]) )
		elif arg=='-g' or arg=='--groupby':
			i += 1
			conf.groupby = sys.argv[i]
		elif arg=='-gs' or arg=='--groupsort':
			i += 1
			conf.groupsort = sys.argv[i]
		elif arg=='-l' or arg=='--limit':
			i += 1
			conf.limit = int(sys.argv[i])
		else:
			conf.q = '%s%s' % ( conf.q, arg )
		i += 1

cl = SphinxClient()
def doQuery(sentence = ""):
	print sentence
	sentence = '|'.join(cmmseg.segment(sentence.encode("utf8")))
	ret = []
	# do query
	cl.SetServer ( conf.sphinx_host, conf.sphinx_port )
	cl.SetWeights ( [100, 1] )
	cl.SetMatchMode ( conf.mode )
	cl.SetRankingMode(conf.rankmode)
	if conf.filtervals:
		cl.SetFilter ( conf.filtercol, conf.filtervals )
	if conf.groupby:
		cl.SetGroupBy ( conf.groupby, SPH_GROUPBY_ATTR, conf.groupsort )
	if conf.sortby:
		cl.SetSortMode ( SPH_SORT_ATTR_DESC, conf.sortby )
	if conf.limit:
		cl.SetLimits ( 0, conf.limit, max(conf.limit,100000) )
	res = cl.Query ( sentence, conf.index )

	if not res:
		print 'query failed: %s' % cl.GetLastError()
		sys.exit(1)

	if cl.GetLastWarning():
		print 'WARNING: %s\n' % cl.GetLastWarning()

	print 'Query \'%s\' retrieved %d of %d matches in %s sec' % (conf.q, res['total'], res['total_found'], res['time'])
	print 'Query stats:'

	if res.has_key('words'):
		for info in res['words']:
			print '\t\'%s\' found %d times in %d documents' % (info['word'], info['hits'], info['docs'])
	print res
	if res.has_key('matches'):
		n = 1
		print '\nMatches:'
		matches_sorted = sorted(res['matches'], key=lambda k:k['weight'], reverse=True)
		print matches_sorted
		for i in range(min(conf.outputlimit, len(matches_sorted))):
			match = matches_sorted[i]
			oneitem = {"question": "", "answers": []}
			attrsdump = ''
			for attr in res['attrs']:
				attrname = attr[0]
				attrtype = attr[1]
				value = match['attrs'][attrname]
				if attrtype==SPH_ATTR_TIMESTAMP:
					value = time.strftime ( '%Y-%m-%d %H:%M:%S', time.localtime(value) )
				attrsdump = '%s, %s=%s' % ( attrsdump, attrname, value )
			hdocid = rediscli.get(conf.docid_rediskey_format % (match['id']	))
			quest = koubeicli.findQuestionByDocid(hdocid)
			oneitem["question"] = quest.content
			oneitem["weight"] = match["weight"]
			print oneitem["question"]
			quest_ans = koubeicli.findQuestionWithAnsersByUrl(quest.docid[:4], quest.post_url)
			if len(quest_ans.answers):
				# row = hbasecli.getRow(hdocid)
				for ans in quest_ans.answers:
					content = {'content':ans.content,'create_time':formatdate(ans.createtime)}
					oneitem["answers"].append(content)
				print oneitem["answers"]
				answers_sorted = sorted(oneitem["answers"], key=lambda k:int(time.mktime(time.strptime(k['create_time'], "%Y-%m-%d %H:%M:%S"))), reverse=False)
				print answers_sorted
				oneitem["answers"] = answers_sorted
					# print '%d. doc_id=%s, hbasedocid=%s, content=%s, weight=%d%s' % (n, match['id'], hdocid, content, match['weight'], attrsdump)
				ret.append(oneitem)
				n += 1

	return ret
if __name__ == '__main__':
	if not sys.argv[1:]:
		Usage()
	parseparam()
	print doQuery(conf.q)
#
# $Id: test.py 2055 2009-11-06 23:09:58Z shodan $
#
