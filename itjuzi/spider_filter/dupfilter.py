# -*- coding:utf-8 -*-
import redis
expire_interval = 60*60*24*2


class DupeFilter():
    """A dupe filter that considers the URL"""

    def __init__(self, path=None, debug=True):
        self.redis_client = redis.StrictRedis(host='localhost', port=6379)

    def request_seen(self, url):
        if self.redis_client.get(url):
            print 'duplicate url： ', url
            return True



    def insert_url(self, url):
        self.redis_client.set(url, '1')
        self.redis_client.expire(url, expire_interval)