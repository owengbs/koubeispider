import json
import urllib
import urllib2
from lxml import etree
req_url = "http://ask.yaolan.com/ajax/getMoreComment"
data = {'qid':'28379613',  'pagenum':'3'}
data = urllib.urlencode(data)
req = urllib2.Request(req_url, data)
res = urllib2.urlopen(req)
the_page = res.read()
the_page_json = json.loads(the_page)
tree = etree.HTML(the_page_json["msg"])
nodes = tree.xpath("//div[@class='expert_box']/div[@class='clear']/div[@class='expert_a']")
for node in nodes:
    author = node.xpath("./div[@class='bar']/a[1]/text()")[0]
    content = node.xpath("./p/text()")[0]
    create_time = node.xpath("./div[@class='bar']/div[@class='r80']/text()")[0]
    print content




