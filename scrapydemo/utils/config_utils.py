import ConfigParser
import os


class ConfigHelper():
    base_path = os.path.dirname(__file__)
    project_path = os.path.dirname(base_path)
    config_path = os.path.join(project_path, 'config', 'db.config')
    cf = ConfigParser.ConfigParser()
    cf.read(config_path)

    @classmethod
    def get_redis_info(cls):
        db_host = cls.cf.get("redis", "redis_host")
        db_port = cls.cf.getint("redis", "redis_port")
        expire_interval_str = cls.cf.get("redis", "expire_interval")
        expire_interval = eval(expire_interval_str)
        return db_host, db_port, expire_interval

    @classmethod
    def get_hbase_info(cls):
        db_host = cls.cf.get("hbase", "hbase_host")
        db_port = cls.cf.getint("hbase", "hbase_port")
        db_table = cls.cf.get("hbase", "hbase_table")
        return db_host, db_port, db_table

    @classmethod
    def get_domain_id(cls, key):
        return cls.cf.get('domain', key)

if __name__ == '__main__':
    print ConfigHelper.get_domain_id('www.mama.cn')
    print ConfigHelper.get_hbase_info()
    print ConfigHelper.get_redis_info()
