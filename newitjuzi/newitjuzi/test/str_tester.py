import urlparse

import re

str = 'https://www.itjuzi.com/investfirm/1'
index = str.rfind('/')
print str[index+1:]