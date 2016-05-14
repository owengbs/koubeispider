import redis
from newitjuzi.utils.config_utils import ConfigUtils


class RedisHelper():
    _redis_client = None
    _redis_info = ConfigUtils.get_redis_info()
    @classmethod
    def get_instance(cls):
        if cls._redis_client:
            return cls._redis_client
        else:
            cls._redis_client = redis.StrictRedis(host=cls._redis_info[0],
                                                   port=cls._redis_info[1])
        return cls._redis_client

