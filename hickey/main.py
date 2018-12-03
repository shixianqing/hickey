from scrapy.cmdline import execute
import re

execute("scrapy crawl country_hickey".split())
# execute("scrapy crawl foreign_hickey".split())

#
# reg = ".*\\/*.txt"
# # reg = ".*content.jsp.*"
# # a = "http://app1.sfda.gov.cn/datasearchcnda/face3/content.jsp?tableId=36&tableName=TABLE36&tableView=%E8%BF%9B%E5%8F%A3%E8%8D%AF%E5%93%81&Id=11573"
# a = "http://app1.sfda.gov.cn/robots.txt"
# flag = re.match(reg, a)
#
# print(flag)