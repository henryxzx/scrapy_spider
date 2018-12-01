# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from urllib import parse
from ArticleSpider.items import JobBoleArticleItem, ArticleItemLoader
from ArticleSpider.utils.common import get_md5
import datetime
from scrapy.loader import ItemLoader


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']
    '''
    提取当前页所有文章的url 一页20个 并获取下一页的url
    '''
    def parse(self, response):
        res_nodes = response.css('.post.floated-thumb .post-thumb a')
        for post_node in res_nodes:
            image_url = post_node.css('img::attr(src)').extract_first('')
            post_url = post_node.css('::attr(href)').extract_first('')
            yield Request(url=parse.urljoin(response.url, post_url), meta={'front_image_url':image_url}, callback=self.parse_detail)

        next_url = response.css('.next.page-numbers::attr(href)').extract_first('')
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    '''
    提取文章具体数据
    '''
    def parse_detail(self, response):
        Article_item = JobBoleArticleItem()
        # res_image_url = response.meta.get('front_image_url', '')
        # res_title = response.css('.entry-header h1::text').extract_first('')
        # res_date = response.css('p.entry-meta-hide-on-mobile::text').extract_first().strip().replace(' ·', '')
        # try:
        #     res_date = datetime.datetime.strptime(res_date, '%Y/%m/%d').date()
        # except Exception as e:
        #     res_date = datetime.datetime.now().date()
        #
        # res_praise = response.css('.vote-post-up h10::text').extract_first('')
        # res_collection = response.css('.bookmark-btn::text').extract_first('')
        # re_res_collection = re.match('.*(\d+).*', res_collection)
        # if re_res_collection:
        #     collection_num = re_res_collection.group(1)
        # else:
        #     collection_num = 0
        # res_comments = response.css('a[href="#article-comment"] span::text').extract_first().strip()
        # re_res_comments = re.match('.*(\d+).*', res_comments)
        # if re_res_comments:
        #     comments_num = re_res_comments.group(1)
        # else:
        #     comments_num = 0
        #
        # res_title = response.css('.entry-header h1::text').extract_first('')
        # res_content = response.css('div.entry').extract_first()
        # res_tag_list = response.css('.entry-meta-hide-on-mobile a::text').extract()
        # tags = ", ".join(res_tag_list)



        # title = scrapy.Field()
        # create_date = scrapy.Field()
        # url = scrapy.Field()
        # url_md5 = scrapy.Field()
        # front_image_url = scrapy.Field()
        # front_image_path = scrapy.Field()
        # comments_nums = scrapy.Field()
        # tags = scrapy.Field()
        # content = scrapy.Field()
        # collection_nums = scrapy.Field()
        # praise_nums = scrapy.Field()
        #
        # Article_item['title'] = res_title
        # Article_item['create_date'] = res_date
        # Article_item['url'] = response.url
        # Article_item['url_md5'] = get_md5(response.url)
        # Article_item['front_image_url'] = [res_image_url]
        # Article_item['comments_nums'] = comments_num
        # Article_item['tags'] = tags
        # Article_item['content'] = res_content
        # Article_item['collection_nums'] = collection_num
        # Article_item['praise_nums'] = res_praise

        #通过item_loader加载
        res_image_url = response.meta.get('front_image_url', '')
        item_loader = ArticleItemLoader(item=JobBoleArticleItem(), response=response)
        item_loader.add_css('title', '.entry-header h1::text')
        item_loader.add_value('url', response.url)
        item_loader.add_value('url_md5', get_md5(response.url))
        item_loader.add_css('create_date', 'p.entry-meta-hide-on-mobile::text')
        item_loader.add_value('front_image_url', [res_image_url])
        item_loader.add_css('comments_nums', 'a[href="#article-comment"] span::text')
        item_loader.add_css('tags', '.entry-meta-hide-on-mobile a::text')
        item_loader.add_css('content', 'div.entry')
        item_loader.add_css('collection_nums', '.bookmark-btn::text')
        item_loader.add_css('praise_nums', '.vote-post-up h10::text')

        Article_item = item_loader.load_item()

        yield Article_item
