# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import HtmlResponse
from selenium.common.exceptions import TimeoutException
import time

class HickeySpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from hickey.util.fileUtil import writeFile
from scrapy.selector import Selector
class HickeyDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        s.fail_path = crawler.settings.get("FAIL_LOG_PATH")
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        url = request.url
        try:
            spider.browser.get(url)
            # WebDriverWait(spider.browser, 5).until(EC.presence_of_element_located((By.ID, "pageForm")))
        except TimeoutException as e:
            print("{}--------》》》超时了，记录下来".format(url))
            writeFile(url, self.fail_path)
            return request
            # spider.browser.execute_script('window.stop()')
        time.sleep(2)
        html = spider.browser.page_source
        selector = Selector(text=html)
        title = selector.xpath('//*[@id="content"]/div/div/table[1]/tbody/tr[1]/td/div[1]').extract_first()
        pageNo = selector.xpath('//*[@id="content"]/table[4]/tbody/tr/td[1]').extract_first()
        if not title and not pageNo:
            print("{}--------页面没有渲染成功".format(url))
            return request
        # spider.browser.close()
        return HtmlResponse(url=url, body=html, encoding="utf-8",
                            request=request)

    def process_response(self, request, response, spider):
        url = response.url
        writeFile(url, "url.txt")

        if response.status != 200 :
            print("{}-------->>>>>>的响应码为{}，有问题，需要记录".format(url,response.status))
            writeFile(url=url, fileName=self.fail_path)
            return request
        return response

    def process_exception(self, request, exception, spider):

        url = request.url

        print("{}--------》》请求出现异常--------".format(url))
        writeFile(url=url, fileName=self.fail_path)
        return request
        pass


    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
