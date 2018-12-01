# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class LagouSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['http://www.lagou.com/']

    agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/" \
            "537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"
    custom_settings = {
        "COOKIES_ENABLED": False,
        "DOWNLOAD_DELAY": 1,
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Cookie': 'JSESSIONID=ABAAABAAAIAACBI79B32EA506A384A3F6C2F260F066ABBB; _ga=GA1.2.683728739.1540463321; user_trace_token=20181025182841-be26feaa-d840-11e8-812e-5254005c3644; LGUID=20181025182841-be2705cf-d840-11e8-812e-5254005c3644; index_location_city=%E6%B7%B1%E5%9C%B3; TG-TRACK-CODE=index_hotjob; X_HTTP_TOKEN=60cfc31237350bee988cceb42c253bce; LGSID=20181026125252-feaddb46-d8da-11e8-821d-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2F; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2F5260699.html%3Fsource%3Dhome_hot%26i%3Dhome_hot-0; X_MIDDLE_TOKEN=8e59066e44ae66052baa91362bd7e15d; SEARCH_ID=787def6578f94c21bd0cd212661cdc52; LGRID=20181026131421-ff012b29-d8dd-11e8-821e-5254005c3644',
            'Host': 'www.lagou.com',
            'Origin': 'https://www.lagou.com',
            'Referer': 'https://www.lagou.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        }
    }

    rules = (
        Rule(LinkExtractor(allow=('zhaopin/.*',)), follow=True),
        Rule(LinkExtractor(allow=('gongsi/j\d+.html')),follow=True),
        Rule(LinkExtractor(allow=r'jobs/\d+.html'), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        i = {}
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return i
