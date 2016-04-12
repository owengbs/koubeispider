import urllib2
from lxml import etree
def parse_itjuzi(html):
    tree = etree.HTML(html)
    print tree
    nodes = tree.xpath("/html/body/div[2]/div[1]/div[2]/div[3]/div/div[1]/ul[2]/li[1]/i[2]/p[1]/a/span")
    print nodes

response = urllib2.urlopen("https://www.itjuzi.com/investfirm")
html = response.read()
parse_itjuzi(html)
open("itjuzi.1.html", "w").write(html)
pageno = 2
while response:
    response = urllib2.urlopen("https://www.itjuzi.com/investfirm?page=%d" % (pageno))
    html = response.read()
    open("itjuzi.%d.html" % (pageno), "w").write(html)
    pageno += 1
    print "len:%d page%d" % (len(html), pageno)