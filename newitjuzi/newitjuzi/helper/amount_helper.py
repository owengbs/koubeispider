# -*- coding:utf-8 -*-
from newitjuzi.utils.config_utils import ConfigUtils


class AmountHelper():
    symbol_dict = ConfigUtils.get_symbol_dict()

    @classmethod
    def convertAmount(cls, amountmsg):
        symbol_list = cls.symbol_dict.keys()
        symbol_msg = ''
        symbol_value = -1
        amount = -1
        for i in range(len(symbol_list)):
            if amountmsg.endswith(symbol_list[i]):
                symbol_msg = symbol_list[i]
                symbol_value = cls.symbol_dict[symbol_msg]
                break
        index = amountmsg.rindex(symbol_msg)
        amount = amountmsg[0:index]
        if len(amount) == 0:
            amount = -1
        elif amount == '亿元及以上':
            amount = 10000
        elif amount == '数千万':
            amount = 5000
        elif amount == '数百万':
            amount = 500
        elif amount == '数十万':
            amount = 50
        elif amount.endswith('亿'):
            amount = amount.replace('亿', '')
            amount = float(amount) * 10000
        elif amount.endswith('万'):
            amount = amount.replace('万', '')
        else:
            raise NameError('Error amounmsg: ', amountmsg)
        return amount, symbol_value
