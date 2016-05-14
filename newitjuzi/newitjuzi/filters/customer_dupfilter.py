# -*- coding: utf-8 -*-
from scrapy.dupefilters import RFPDupeFilter
from newitjuzi.helper.redis_helper import RedisHelper
from newitjuzi.utils.config_utils import ConfigUtils


class CustomDupFilter(RFPDupeFilter):
    expire_interval = ConfigUtils.get_redis_info()[2]

    def __init__(self, path=None, debug=True):
        self.redis_client = RedisHelper.get_instance()
        RFPDupeFilter.__init__(self, path, debug)

    def request_seen(self, request):
        request_url = request.url
        if self.redis_client.get(request_url):
            return True
        else:
            self.redis_client.set(request_url, '1')
            self.redis_client.expire(request_url, self.expire_interval)
