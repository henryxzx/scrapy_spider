# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse
from ArticleSpider.items import GameItem, ArticleItemLoader

class GamespiderSpider(scrapy.Spider):
    name = 'gameSpider'
    allowed_domains = ['www.3dmgame.com']
    start_urls = ['https://www.3dmgame.com/games/zq/']

    def parse(self, response):
        res_nodes = response.css('.ztliswrap .lis .img')
        for post_node in res_nodes:
            image_url = post_node.css('img::attr(src)').extract_first('')
            post_url = post_node.css('::attr(href)').extract_first('')
            yield Request(url=parse.urljoin(response.url, post_url), meta={'front_image_url':image_url}, callback=self.parse_detail)

        next_url = response.css('.ztliswrap .pagewrap .pagination .next a::attr(href)').extract_first('')
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)
        pass

    # #封面图
    # image = response.css('.ztliswrap .lis .img img::attr(src)').extract_first()
    # #游戏url
    # url = response.css('.ztliswrap .lis .img::attr(href)').extract_first()
    #
    #
    # #详情页
    #
    # #游戏标题
    # title = response.css('.ZQ_Left .Gminfo .info .bt h1::text').extract_first()
    # #游戏详情
    # content = response.css('.ZQ_Left .buy .miaoshu::text').extract_first()
    # #发售日期
    # time = response.css('.ZQ_Left .Gminfo .info .lis li::text').extract()[0]
    # #游戏类型
    # type = response.css('.ZQ_Left .Gminfo .info .lis li::text').extract()[1]
    # #游戏发行商
    # publisher = response.css('.ZQ_Left .Gminfo .info .lis li::text').extract()[3]
    # #游戏评分
    # score = response.css('.ZQ_Left .score-box .processingbar font::text').extract_first()

    '''
    提取游戏具体数据
    '''
    def parse_detail(self, response):
        Game_item = GameItem()
        #通过item_loader加载
        res_image_url = response.meta.get('front_image_url', '')
        item_loader = ArticleItemLoader(item=GameItem(), response=response)
        item_loader.add_css('title', '.ZQ_Left .Gminfo .info .bt h1::text')
        item_loader.add_value('url', response.url)
        item_loader.add_css('time', '.ZQ_Left .Gminfo .info .lis li::text')
        item_loader.add_value('front_image_url', [res_image_url])
        item_loader.add_css('content', '.ZQ_Left .buy .miaoshu::text')
        item_loader.add_css('type', '.ZQ_Left .Gminfo .info .lis li::text')
        item_loader.add_css('publisher', '.ZQ_Left .Gminfo .info .lis li::text')
        item_loader.add_css('score', '.ZQ_Left .score-box .processingbar font::text')
        Game_item = item_loader.load_item()

        yield Game_item
