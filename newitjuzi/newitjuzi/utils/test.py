import ConfigParser
import os

class TUtils():
    cf = ConfigParser.ConfigParser()
    config_path = os.path.split(os.path.realpath(__file__))[0] + '/db.config'
    print config_path
    cf.read(config_path)

    @classmethod
    def get_db_info(cls):

        db_host = cls.cf.get("db", "db_host")
        db_port = cls.cf.getint("db", "db_port")
        db_user = cls.cf.get("db", "db_user")
        db_pwd = cls.cf.get("db", "db_password")
        db_datadb = cls.cf.get("db", "db_database")
        return db_host, db_port, db_user, db_pwd, db_datadb

    @classmethod
    def get_redis_info(cls):
        db_host = cls.cf.get("redis", "redis_host")
        db_port = cls.cf.getint("redis", "redis_port")
        expire_interval_str = cls.cf.get("redis", "expire_interval")
        expire_interval = eval(expire_interval_str)
        return db_host, db_port, expire_interval

    @classmethod
    def get_symbol_info(cls):
        symbol_dict = dict()
        symbol_info = cls.cf.items('symbol')
        for each in symbol_info:
            symbol_dict[each[0]] = each[1]
        ks = symbol_dict.keys()
        symbol_dict.get(key=ks[0])
        return symbol_dict


if __name__ == "__main__":
    print TUtils.get_symbol_info().keys()
    print TUtils.get_db_info()






