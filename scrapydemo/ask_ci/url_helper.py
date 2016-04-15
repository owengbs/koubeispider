import redis
expire_interval = 60*60*24*2

class ParseHelper():
    """A dupe filter that considers the URL"""
    _domain = "http://ask.ci123.com"
    suffix = '-suffix'
    def __init__(self, path=None, debug=True):
        self.redis_client = redis.StrictRedis(host='localhost', port=6379)

    def insert_datetime(self, url, dateTime_obj):
        url = self._domain + url + self.suffix
        self.redis_client.set(url, dateTime_obj)
        self.redis_client.expire(url, expire_interval)

    def get_datetime(self, url):
        return self.redis_client.get(url)


