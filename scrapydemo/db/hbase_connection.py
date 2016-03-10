from thrift.transport import TSocket


from hbase import Hbase
from hbase.ttypes import *
class dbconenection():

    def __init__(self):    	
    	if self.client ==null:
    		print 'dbconenection init ......'
	    	tsocket = TSocket.TSocket('localhost', 9090)
	    	transport = TTransport.TBufferedTransport(tsocket)
	    	protocol = TBinaryProtocol.TBinaryProtocol(transport)
	    	self.client = Hbase.Client(protocol)
	    	transport.open()
	    	
    def insert_data(self, item):
		row = 'row-key1'
		author = Mutation(column="attributes:author", value=item['author'])
		create_time = Mutation(column="attributes:create_time", value=item['create_time'])
		from_url=Mutation(column="attributes:from_url", value=item['from_url'])
		post_url = Mutation(column="attributes:post_url", value=item['post_url'])
		rank = Mutation(column="attributes:rank", value=item['rank'])	
		title=Mutation(column="attributes:title", value=item['title'])
		content_type = Mutation(column="attributes:content_type", value=item['content_type'])
		content = Mutation(column="content:", value=item['content'])
		mutations = [Mutation(column="attr:title", value="test title"),Mutation(column="attr:link", value="test link"),Mutation(column="content:c", value="test content")]
		client.mutateRow('shane', row, mutations, None)


