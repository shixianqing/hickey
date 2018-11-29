from redis.client import Redis
from redis.connection import Connection,ConnectionPool
from scrapy.utils.project import get_project_settings
class Jedis():

    """"
        host:ip地址
        port: 端口号
        pwd:密码
        db:数据库索引
    """
    def __init__(self, host=None, port=None, pwd=None, db=None):

        self.client = Redis(host=get_project_settings().get("REDIS_HOST"),port=get_project_settings().get("REDIS_PORT"))
        # self.client = StrictRedis(ConnectionPool(Connection(host=host,port=port,db=db,password=pwd)))

    def addUrl(self, key, val):
        r = self.client.set(key,val)
        print(self.client.get(key))



