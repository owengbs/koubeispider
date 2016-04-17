# -*- coding: utf-8 -*-
from scrapy.dupefilter import RFPDupeFilter
import redis

expire_interval = 60*60*12


class CustomDupeFilter(RFPDupeFilter):
    """A dupe filter that considers the URL"""

    def __init__(self, path=None, debug=True):
        self.redis_client = redis.StrictRedis(host='localhost', port=6379)
        RFPDupeFilter.__init__(self, path, debug)

    def request_seen(self, request):
        request_url = request.url
        if self.redis_client.get(request_url):
            return True
        else:
            self.redis_client.set(request_url, '1')
            self.redis_client.expire(request_url, expire_interval)

    def __def__(self):
        self.redis_client.shutdown()
