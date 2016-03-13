from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

from hbase import Hbase
from hbase.ttypes import *

class HbaseBase(object):
    def __init__(self):
        self.tableName = 'demo'    
        transport = TSocket.TSocket('localhost', 9090)
        transport = TTransport.TBufferedTransport(transport)
        protocol = TBinaryProtocol.TBinaryProtocol(transport)
        transport.open()
        self.client = Hbase.Client(protocol)
    def getRow(self, rowKey='', attributes=None):        
        result = self.client.getRow(self.tableName, rowKey, attributes)[0].columns
        ret = {}
        for item in result.iteritems():
            if item:
                ret[item[0]] = item[1].value
        return ret
    def scanByRange(self, startrow = '', stoprow = '', columns = None):
        scanid = self.client.scannerOpenWithStop(self.tableName, startrow, stoprow, columns, None)
        ret = []
        while True:
            rows = self.client.scannerGetList(scanid, 1)
            if len(rows) == 0:
                break
            for row in rows:
                onerow = {}
                for item in row.columns.iteritems():
                    onerow[item[0]] = item[1].value
                ret.append(onerow)
        return ret
    def insertRow(self, rowKey='',values={}):
        mutations = []
        for item in values.iteritems():    
            mutations.append(Mutation(column=item[0],value=item[1]))
        return self.client.mutateRow(self.tableName,rowKey,mutations, None)
if __name__ == '__main__':
    base = HbaseBase()
    # ret = base.getRow('fe244f01f3d82068578d0346dd29b179')
    # ret = base.scanByRange('ee244f01f3d82068578d0346dd29b179','ffffff01f3d82068578d0346dd29b179')
    print base.insertRow("0001dc362f838bdab14ede19d0fa8e419388dc487a852a9e349a012ad8ec503c9a7a",{"content1:newcolumn":"asdsadas"})
    # print ret 
