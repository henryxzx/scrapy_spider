import requests
from os import path
import os
import http.cookiejar
agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'

header = {
    'HOST' : 'www.zhihu.com',
    'referer' : 'https://www.zhihu.com/',
    'user-agent' : agent
}

from selenium import webdriver
import time

options = webdriver.ChromeOptions()
options.add_argument('lang=zh_CN.UTF-8')
options.add_argument('user-agent="Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20"')
browser = webdriver.Chrome(chrome_options=options)
# browser = webdriver.Chrome()

browser.get("https://www.zhihu.com/signin")
browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(
        "13760710096")
time.sleep(1)
browser.find_element_by_css_selector(".SignFlow-password input").send_keys(
        "XQY1197966810G")
time.sleep(2)
browser.find_element_by_css_selector(
        ".Button.SignFlow-submitButton").click()
time.sleep(3)
browser.get("https://www.zhihu.com/")

time.sleep(6)
zhihu_cookies = browser.get_cookies()
print("aaa", zhihu_cookies)
cookie_dict = {}
import pickle
for cookie in zhihu_cookies:
    base_path = path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'cookies')
    print(base_path)
    f = open(base_path + "/zhihu/" + cookie['name'] + '.zhihu', 'wb')
    pickle.dump(cookie, f)
    f.close()
    cookie_dict[cookie['name']] = cookie['value']
browser.close()
