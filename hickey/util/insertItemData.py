# -*- coding: utf-8 -*-
from hickey.dbtool import MysqlPool
from hickey.util.redisUtil import Jedis
import json

jedis = Jedis()
pool = MysqlPool()
def getItem(start,end):
    items = jedis.client.lrange("country_hickey:items",start=start,end=end)
    params = []
    for item in items:
        item = json.loads(item.decode("utf-8"))
        params.append(tuple(list(item["info"])))
    insert_data(params=params)
    print("{}------{}".format(start,end))


def insert_data(params):
    try:
        sql = "INSERT INTO `scrapy_dev`.`country_hickey` ( `registry_cert_no`, `registry_per_name`, " \
              "`registry_per_addr`, `prod_addr`, `proxy_per_name`, `proxy_per_addr`, `prod_name`, `standard`," \
              " `structure`, `apply_limit`, `other_content`, `remark`, `allow_date`, `effective_date`, `enclosure`, " \
              "`prod_standard`, `change_date`, `post_no`, `component`, `expect_use`, `prod_save_conditon`, `auth_dept`," \
              " `change_situation`)" \
              " VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s," \
              " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        pool.insertMany(sql=sql,values=params)
        pool.end("commit")
        print("插入成功")
    except BaseException as e:
        print("{}".format(e))
        print("插入失败---------->>>{}".format(params))

def main():
    for i in range(1,149):
        start,end = 0,0
        if i == 1:
            start = (i - 1) * 1000
            end = start + 1000
        else:
            start = (i - 1) * 1000+1
            end = start + 999
        getItem(start=start,end=end)
        # print("{}------{}".format(start, end))


if __name__ == '__main__':
    main()
    pool.release_conn()
    # insert_data()