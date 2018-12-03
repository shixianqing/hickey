# -*- coding: utf-8 -*-
# from scrapy.spider import CrawlSpider,Rule
# from scrapy.linkextractor import LinkExtractor
from scrapy.selector import Selector
from scrapy.http.request import Request
from selenium import webdriver
from hickey.items import HickeyItem
from hickey.items import ForeignHickeyItem
from scrapy_redis.spiders import RedisSpider
from hickey.util.redisUtil import Jedis
import re

'''
国产器械
'''
class CountryHickeySpider(RedisSpider):

    name = 'country_hickey'
    allowed_domains = ['http://app1.sfda.gov.cn']
    url_pattern = 'http://app1.sfda.gov.cn/datasearchcnda/face3/search.jsp?bcId=152904417281669781044048234789&'\
                  'curstart={}&tableName=TABLE26&State=1&tableId=26&tableView=%E5%9B%BD%E4%BA%A7%E5%99%A8%E6%A2%B0'

    redis_key = 'countryHickey:start_urls'
    start_url = "http://app1.sfda.gov.cn/datasearchcnda/face3/search.jsp?tableId=27&bcId=152904442584853439006654836900"
    # for i in range(1, 9812):Jedis().client.lpush(redis_key, url.format(i))

    def __init__(self, *args, **kwargs):
        self.browser = webdriver.Chrome()
        # self.browser.set_page_load_timeout(30)

    def parse(self, response):
        html = response.body.decode("utf-8")
        select = Selector(text=html)
        url = response.url
        if url == self.start_url:
            click_url = select.xpath("/html/body/table[4]/tbody/tr/td[6]/img/@onclick").extract_first()
            totalPage = int("".join(re.findall("[0-9]", click_url)))
            for i in range(1, totalPage + 1): yield Request(url=self.url_pattern.format(i), callback=self.parse,
                                                            dont_filter=True)
        else:
            a_el_list = select.xpath("/html/body/table[2]/tbody/tr/td/p/a/@href").extract()
            for a_el in a_el_list:
                u = "http://app1.sfda.gov.cn/datasearchcnda/face3/" + a_el.split(",")[1].replace("'", "")
                self.log("detail_url------------->>>{}".format(u))
                yield Request(url=u, callback=self.parse_item, dont_filter=True)

    def parse_item(self,response):
        select = Selector(text=response.body.decode("utf-8"))
        tdList = select.xpath("/html/body/div/div/table[1]/tbody/tr/td[2]")
        texts = []
        for k, td in enumerate(tdList):
            if k > 22: break
            text = td._root.text
            texts.append(text if text is not None else "")
        item = HickeyItem()
        item["info"] = texts
        item["url"] = response.url
        yield item

    def start_requests(self):
        yield Request(url=self.start_url, callback=self.parse, dont_filter=True)



'''
进口器械
'''
class ForeignHickeySpider(RedisSpider):

    name = 'foreign_hickey'
    allowed_domains = ['http://app1.sfda.gov.cn']
    url_pattern = 'http://app1.sfda.gov.cn/datasearchcnda/face3/search.jsp?tableId=27&State=1&' \
          'bcId=152904442584853439006654836900&State=1&curstart={}&State=1&' \
          'tableName=TABLE27&State=1&viewtitleName=COLUMN200&State=1&viewsubTitleName=COLUMN192,COLUMN199&State=1' \
          '&tableView=%25E8%25BF%259B%25E5%258F%25A3%25E5%2599%25A8%25E6%25A2%25B0&State=1&cid=0' \
          '&State=1&ytableId=0&State=1&searchType=search&State=1'
    start_url = "http://app1.sfda.gov.cn/datasearchcnda/face3/search.jsp?tableId=27&bcId=152904442584853439006654836900"
    redis_key = 'foreignHickey:start_urls'
    # for i in range(1, 3355):Jedis().client.lpush(redis_key, url.format(i))

    def __init__(self, *args, **kwargs):
        self.browser = webdriver.Chrome()

    def parse(self, response):
        select = Selector(text=response.text)
        url = response.url
        if url == self.start_url:
            click_url = select.xpath("/html/body/table[4]/tbody/tr/td[6]/img/@onclick").extract_first()
            totalPage = int("".join(re.findall("[0-9]", click_url)))
            for i in range(1, totalPage + 1): yield Request(url=self.url_pattern.format(i), callback=self.parse,
                                                            dont_filter=True)
        else:
            a_el_list = select.xpath("/html/body/table[2]/tbody/tr/td/p/a/@href").extract()
            for a_el in a_el_list:
                u = "http://app1.sfda.gov.cn/datasearchcnda/face3/" + a_el.split(",")[1].replace("'", "")
                self.log("detail_url------------->>>{}".format(u))
                yield Request(url=u, callback=self.parse_item, dont_filter=True)

    def parse_item(self, response):
        select = Selector(text=response.text)
        tdList = select.xpath("/html/body/div/div/table[1]/tbody/tr/td[2]")
        texts = []
        for k, td in enumerate(tdList):
            if k > 26: break
            text = td._root.text
            texts.append(text if text is not None else "")
        item = ForeignHickeyItem()
        item["info"] = texts
        item["url"] = response.url
        yield item

    def start_requests(self):
        yield Request(url=self.start_url, callback=self.parse, dont_filter=True)
