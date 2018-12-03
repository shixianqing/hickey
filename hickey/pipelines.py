# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from hickey.dbtool import MysqlPool
from hickey.items import HickeyItem
from hickey.items import ForeignHickeyItem
from hickey.util.fileUtil import writeFile, writeDataIntoExcel
from scrapy.utils.project import get_project_settings
from scrapy.exceptions import DropItem
from hickey.items import ForeignHickeyItem

class HickeyPipeline(object):


    def process_item(self, item, spider):

        # medicineInfo = tuple(item["info"])

        url = item["url"]
        if not item["info"]:
            print("{}未获取到数据，url需要记录---------------".format(url))
            writeFile(url=url,fileName=get_project_settings().get("FAIL_LOG_PATH"))
            raise DropItem("{}-----获取得数据为空，丢弃-------".format(url))

        # if isinstance(item,ForeignHickeyItem):
        #     self.process_foreign_hickey(item)
        # else:
        #     self.process_country_hickey(item)
        # if isinstance(item,HickeyItem):
        #     self.process_country_item(medicineInfo, url)
        # elif isinstance(item,ForeignHickeyItem):
        #     self.process_foreign_item(medicineInfo, url)
        return item

    def process_foreign_item(self, info, url):
        try:
            sql = "INSERT INTO `scrapy_dev`.`foreign_hickey` (`prod_name`, `registry_cert_no`, `registry_per_name`, " \
                  "`registry_per_addr`, `product_addr`, `proxy_per_name`, `proxy_per_addr`, `standard`, `structure`, " \
                  "`apply_limit`, `en_product_area`, `enclosure`, `other_conmment`, `remark`, `allow_date`, " \
                  "`effective_date`, `prod_comp_name`, `zh_prod_name`, `prod_standard`, `zh_product_area`, " \
                  "`service_org`, `change_date`, `component`, `expect_use`, `prod_save_conditon`, `auth_dept`," \
                  " `change_situation`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, " \
                  "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                  " %s, %s, %s, %s);"
            self.pool.insert(sql=sql, param=info)
            self.pool.end("commit")
            print("{}---------插入成功----".format(url))
        except BaseException as e:
            print("{}-----插入失败，失败原因----{}".format(url, e))
            writeFile(url, get_project_settings().get("FAIL_LOG_PATH"))


    def process_country_item(self,info, url):
        sql = "INSERT INTO `scrapy_dev`.`country_hickey` ( `registry_cert_no`, `registry_per_name`, " \
              "`registry_per_addr`, `prod_addr`, `proxy_per_name`, `proxy_per_addr`, `prod_name`, `standard`," \
              " `structure`, `apply_limit`, `other_content`, `remark`, `allow_date`, `effective_date`, `enclosure`, " \
              "`prod_standard`, `change_date`, `post_no`, `component`, `expect_use`, `prod_save_conditon`, `auth_dept`," \
              " `change_situation`)" \
              " VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s," \
              " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        try:
            self.pool.insert(sql=sql, param=info)
            self.pool.end("commit")
            print("{}---------插入成功----".format(url))
        except BaseException as e:
            print("{}-----插入失败，失败原因----{}".format(url,e))
            writeFile(url, get_project_settings().get("FAIL_LOG_PATH"))



    """
    
    数据处理前回调该方法，初始化相关操作，比如数据库链接
    
    """
    def open_spider(self,spider):

        # self.pool = MysqlPool()
        pass

    """"
    
    数据完全处理完之后，回调该方法，释放资源
    """
    def close_spider(self,spider):

        # self.pool.release_conn()
        pass


    def process_foreign_hickey(self, item):
        '''
        处理进口器械
        :param item:
        :return:
        '''
        print("-----------------------处理进口器械------------------")
        title = ["产品名称", "注册证编号", "注册人名称", "注册人住所", "生产地址", "代理人名称", "代理人住所", "型号、规格", "结构及组成", "适用范围",
                 "生产国或地区（英文）", "附件", "其他内容", "备注", "批准日期", "有效期至", "生产厂商名称（中文）", "产品名称（中文）",
                 "产品标准", "生产国或地区（中文）", "售后服务机构", "变更日期", "主要组成成分（体外诊断试剂）", "预期用途（体外诊断试剂）",
                 "产品储存条件及有效期（体外诊断试剂）", "审批部门", "变更情况"]
        try:
            writeDataIntoExcel(data=item["info"], tilte=title, fileName=get_project_settings().get("FOREIGE_HICKEY_FILE"))
            print("------------进口器械写入文件成功--------")
        except BaseException as e:
            print("进口器械写入文件异常-------{}".format(e))
            writeFile(url=item["url"], fileName=get_project_settings().get("FAIL_LOG_PATH"))

    def process_country_hickey(self, item):

        '''
        处理国产器械
        :param item:
        :return:
        '''

        print("-----------------------处理国产器械------------------")
        title = ["注册证编号", "注册人名称", "注册人住所", "生产地址", "代理人名称", "代理人住所", "产品名称", "型号、规格", "结构及组成",
                 "适用范围", "其他内容", "备注", "批准日期", "有效期至", "附件", "产品标准", "变更日期",
                 "邮编", "主要组成成分（体外诊断试剂）", "预期用途（体外诊断试剂）", "产品储存条件及有效期（体外诊断试剂）", "审批部门", "变更情况"]
        try:
            writeDataIntoExcel(data=item["info"], tilte=title,
                               fileName=get_project_settings().get("COUNTRY_HICKEY_FILE"))
            print("------------国产器械写入文件成功--------")
        except BaseException as e:
            print("国产器械写入文件异常-------{}".format(e))
            writeFile(url=item["url"], fileName=get_project_settings().get("FAIL_LOG_PATH"))

