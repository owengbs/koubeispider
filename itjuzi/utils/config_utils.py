import ConfigParser
import os


class ConfigUtils():
    source_path = os.getcwd()
    project_path = os.path.dirname(source_path)

    @classmethod
    def get_db_info(cls):
        cf = ConfigParser.ConfigParser()
        source_path = os.path.join(cls.source_path, 'config', 'db.config')
        cf.read(source_path)
        db_host = cf.get("db", "db_host")
        db_port = cf.getint("db", "db_port")
        db_user = cf.get("db", "db_user")
        db_pwd = cf.get("db", "db_password")
        db_datadb = cf.get("db", "db_database")
        return db_host, db_port, db_user, db_pwd, db_datadb


if __name__ == '__main__':
    infos = ConfigUtils.get_db_info()
    print infos[0]
    print infos[1]
    print infos[2]
    print infos[3]
