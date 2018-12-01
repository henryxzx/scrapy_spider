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
    create_date = scrapy.Field(
        input_processor=MapCompose(date_convert)
    )
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


class LagouJobItemLoader(ItemLoader):



class LagouJobItem(scrapy.Item):
    url = scrapy.Field(

    )
    url_object_id = scrapy.Field()


    pass
