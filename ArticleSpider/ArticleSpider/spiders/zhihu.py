# -*- coding: utf-8 -*-
import scrapy
import os
from os import path
import re


from urllib import parse


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']
    agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'
    header = {
        'HOST': 'www.zhihu.com',
        'Referer': 'https://www.zhihu.com',
        'User-Agent': agent
    }

    def parse(self, response):
        all_urls = response.css('a::attr(href)').extract()
        all_urls = [parse.urljoin(response.url, url) for url in all_urls]
        pass

    def start_requests(self):
        from selenium import webdriver
        import time
        driver = webdriver.Chrome()
        driver.get('https://www.zhihu.com/signin')
        driver.find_element_by_css_selector('.SignFlow-accountInput.Input-wrapper input').send_keys('13760710096')
        time.sleep(1)
        driver.find_element_by_css_selector('.Input-wrapper input').send_keys('XQY1197966810g')
        time.sleep(2)
        driver.find_element_by_css_selector('Button SignFlow-submitButton Button--primary Button--blue').click()
        time.sleep(3)
        driver.get(self.start_urls)
        time.sleep(5)
        zhihu_cookies = driver.get_cookies()
        cookie_dict = {}
        import pickle
        for cookie in zhihu_cookies:
            base_path = path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'cookies')
            f = open(base_path + '/zhihu/' + cookie['name'] + '.zhihu', 'wb')
            pickle.dump(cookie, f)
            f.close()
            cookie_dict[cookie['name']] = cookie['value']
        driver.close()
        return [scrapy.Request(url=self.start_urls[0], dont_filter=True, cookies=cookie_dict, headers=self.header)]