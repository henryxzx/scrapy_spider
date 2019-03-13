# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import datetime
import re

from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join



def date_convert(value):
    try:
        re_date = value.strip().replace(' ·', '')
        create_date = datetime.datetime.strptime(re_date, '%Y/%m/%d').date()
    except Exception as e:
        create_date = datetime.datetime.now().date()
    return create_date


def get_nums(value):
    match_re = re.match('.*?(\d+).*', value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0
    return nums

def getTime(value):
    match_re = re.match('.*(\d{4}-\d{1,2}-\d{1,2}).*', value)
    if match_re:
        time = match_re.group(1)
    else:
        time = ''
    return time

def getType(value):
    match_re = re.match(".*?类型：(.*).*", value)
    if match_re:
        type = match_re.group(1)
        if(type == '射击游戏' or type == '第一人称射击' or type == '第三人称射击'):
            type = 1
        elif(type == '角色扮演' or type == '冒险游戏'):
            type = 2
        elif(type == '动作游戏' or type == '动作角色'):
            type = 3
        elif(type == '即时战略' or type == '策略游戏'):
            type = 4
        elif(type == '体育运动' or type == '格斗游戏'):
            type = 5
        elif(type == '赛车游戏'):
            type = 6
        elif(type == '模拟经营'):
            type = 7
        else:
            type = 8
    else:
        type = ''
    return type

def getPublisher(value):
    match_re = re.match(".*?发行：(.*).*", value)
    if match_re:
        publisher = match_re.group(1)
    else:
        publisher = ''
    return publisher

def getScore(value):
    match_re = re.match('.*?(\d\.\d).*', value)
    if match_re:
        score = int(float(match_re.group(1)) * 10)
    else:
        score = 0
    return score



def return_value(value):
    return value

def remove_comment_tags(value):
    #去掉tag中提取的评论
    if "评论" in value:
        return
    else:
        return value

class ArticleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


# class jobboleArticlespiderItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     title = scrapy.Field()
#     create_date = scrapy.Field()
#     url = scrapy.Field()
#     url_md5 = scrapy.Field()
#     front_image_url = scrapy.Field()
#     front_image_path = scrapy.Field()
#     comments_nums = scrapy.Field()
#     tags = scrapy.Field()
#     content = scrapy.Field()
#     collection_nums = scrapy.Field()
#     praise_nums = scrapy.Field()


class JobBoleArticleItem(scrapy.Item):
    title = scrapy.Field()
    create_date = scrapy.Field()
    url = scrapy.Field()
    url_md5 = scrapy.Field()
    front_image_url = scrapy.Field(
        output_processor=MapCompose(return_value)
    )
    front_image_path = scrapy.Field()
    praise_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    comments_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    tags = scrapy.Field(
        input_processor=MapCompose(remove_comment_tags),
        output_processor=Join(',')
    )
    content = scrapy.Field()
    collection_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    def get_insert_sql(self):
        sql = '''
            INSERT INTO article(title, create_date, url, url_md5, front_image_url, comments_nums, collection_nums,
            praise_nums, tags, content)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE comments_nums=VALUES(comments_nums),
             collection_nums=VALUES(collection_nums), praise_nums=VALUES(praise_nums)
        '''

        fron_image_url = ""
        if self["front_image_url"]:
            fron_image_url = self["front_image_url"][0]
        params = (self["title"], self["create_date"], self["url"], self['url_md5'],
                  fron_image_url, self["comments_nums"],  self["collection_nums"],
                  self["praise_nums"], self["tags"], self["content"])
        return sql, params


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

class GameItem(scrapy.Item):
    title = scrapy.Field()
    time = scrapy.Field(
        input_processor=MapCompose(getTime)
    )
    url = scrapy.Field()
    front_image_url = scrapy.Field(
        output_processor=MapCompose(return_value)
    )
    content = scrapy.Field()
    type = scrapy.Field(
        input_processor=MapCompose(getType)
    )
    publisher = scrapy.Field(
        input_processor=MapCompose(getPublisher)
    )
    score = scrapy.Field(
        input_processor=MapCompose(getScore)
    )

    def get_insert_sql(self):
        sql = '''
            INSERT INTO game_info(game_name, game_content, game_type_id, game_publisher, game_score, game_publish_time, game_image)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        '''
        fron_image_url = ""
        if self["front_image_url"]:
            fron_image_url = self["front_image_url"][0]
        params = (self["title"], self['content'], self["type"], self["publisher"], self["score"], self["time"], fron_image_url)
        return sql, params


pass


class LagouJobItemLoader(ItemLoader):
    pass



class LagouJobItem(scrapy.Item):
    url = scrapy.Field(

    )
    url_object_id = scrapy.Field()


    pass
