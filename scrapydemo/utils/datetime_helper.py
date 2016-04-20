# -*- coding:utf-8 -*-
import datetime

import re


class DatetimeHelper():
    pattern_0 = re.compile(r"^(\d+?)-(\d+?)-(\d+?) (\d+?):(\d+?):(\d+?)$")
    pattern_1 = re.compile(r"^(\d+?)年(\d+?)月(\d+?)日")
    pattern_2 = re.compile(r"^(\d+?)月(\d+?)日 (\d+):(\d+)$")
    pattern_3 = re.compile(r"^(\d+?)分钟前")
    pattern_4 = re.compile(r"今天 (\d+?):(\d+?)$")
    pattern_5 = re.compile(r"昨天 (\d+?):(\d+?)$")
    pattern_6 = re.compile(r"(\d+?)-(\d+?)-(\d+?) (\d+?):(\d+?)$")
    pattern_7 = re.compile(r"^(\d+?)小时前$")
    pattern_8 = re.compile(r"^(\d+?)天前$")


    format = '%Y-%m-%d %H:%M:%S'


    @classmethod
    def build_datetime_str(cls, datetime_object):
        if datetime_object is None:
            return ''
        datetime_str = ''
        if isinstance(datetime_object, unicode):
            datetime_str = datetime_object.encode("utf-8").strip()
        else:
            datetime_str = datetime_object.strip()

        if datetime_str == '':
            return ''

        matchs = cls.pattern_0.match(datetime_str)
        if matchs:
            return datetime_str

        matchs = cls.pattern_1.match(datetime_str)
        if matchs:
            return datetime.datetime(int(matchs.groups()[0]),
                                     int(matchs.groups()[1]),
                                     int(matchs.groups()[2])).strftime(cls.format)

        now_datetime = datetime.datetime.today()
        matchs = cls.pattern_2.match(datetime_str)
        if matchs:
            year = now_datetime.year
            return datetime.datetime(year, int(matchs.groups()[0]),
                                     int(matchs.groups()[1]),
                                     hour=int(matchs.groups()[2]),
                                     minute=int(matchs.groups()[3])).strftime(cls.format)

        matchs = cls.pattern_3.match(datetime_str)
        if matchs:
            datetime_value = now_datetime - datetime.timedelta(minutes=int(matchs.groups()[0]))
            return datetime_value.strftime(cls.format)

        matchs = cls.pattern_4.match(datetime_str)
        if matchs:
            now_value = now_datetime.replace(hour=int(matchs.groups()[0]),
                                             minute=int(matchs.groups()[1]),
                                             second=0)
            return now_value.strftime(cls.format)

        matchs = cls.pattern_5.match(datetime_str)
        if matchs:
            yesterday = now_datetime - datetime.timedelta(days=1)
            datetime_value = yesterday.replace(hour=int(matchs.groups()[0]),
                                               minute=int(matchs.groups()[1]),
                                               second=0, microsecond=0)
            return datetime_value.strftime(cls.format)

        matchs = cls.pattern_6.match(datetime_str)
        if matchs:
            return datetime.datetime(int(matchs.groups()[0]), int(matchs.groups()[1]),
                                     int(matchs.groups()[2]),
                                     hour=int(matchs.groups()[3]),
                                     minute=int(matchs.groups()[4])).strftime(cls.format)

        matchs = cls.pattern_7.match(datetime_str)
        if matchs:
            datetime_value = now_datetime - datetime.timedelta(hours=int(matchs.groups()[0]))
            return datetime_value.strftime(cls.format)

        matchs = cls.pattern_8.match(datetime_str)
        if matchs:
            datetime_value = now_datetime - datetime.timedelta(days=int(matchs.groups()[0]))
            return datetime_value.strftime(cls.format)






        raise "Invalid datetime format, " , datetime_object

if __name__ == "__main__":
    str =u'2015年12月04日'
    print str, DatetimeHelper.build_datetime_str(str)

    str = '5月21日 14:59'
    print  str, DatetimeHelper.build_datetime_str(str)

    str = "2013年5月21日 14:59"
    print  str, DatetimeHelper.build_datetime_str(str)
    str = '25分钟前'
    print  str, DatetimeHelper.build_datetime_str(str)
    str = '今天 13:29'
    print  str, DatetimeHelper.build_datetime_str(str)
    str = '昨天 23:32'
    print  str, DatetimeHelper.build_datetime_str(str)

    str_2 = '2016-09-10 12:08'
    print  str_2, DatetimeHelper.build_datetime_str(str_2)

    str_2 = '2016-09-10 12:08:56'
    print  str_2, DatetimeHelper.build_datetime_str(str_2)

    str = "3小时前"
    print  str, DatetimeHelper.build_datetime_str(str)
    str ="1天前"

    print  str, DatetimeHelper.build_datetime_str(str)






