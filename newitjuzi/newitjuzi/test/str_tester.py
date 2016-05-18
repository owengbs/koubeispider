# -*- coding: utf-8 -*-
import re

symbol_list=['人民币','美元','欧元','英镑','新台币','其他','未透露']

amountmsg = "899亿美元"
symbol_msg =''
amount = -1
for i in range(len(symbol_list)):
    if amountmsg.endswith(symbol_list[i]):
        symbol_msg = symbol_list[i]
        print i, symbol_list[i]
        break
index = amountmsg.rindex(symbol_msg)
amount =  amountmsg[0:index]
if len(amount)==0:
    amount = -1
elif amount=='亿元及以上':
    amount = 10000
elif amount=='数千万':
    amount = 5000
elif amount =='数百万':
    amount = 500
elif amount=='数十万':
    amount=50
elif amount.endswith('亿'):
    i = len(amount)
    amount = amount.replace('亿','')
    amount = float(amount)*100000000
elif amount.endswith('万'):
    i = len(amount)
    amount = amount.replace('万','')

print amount, symbol_msg






