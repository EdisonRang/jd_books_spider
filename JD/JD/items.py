# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdItem(scrapy.Item):
    # define the fields for your item here like:
    big_category = scrapy.Field()       # 首页大分类名
    big_category_link = scrapy.Field()      # 大分类链接
    small_category = scrapy.Field()     # 首页小分类
    small_category_link = scrapy.Field()        # 小分类链接

    book_name = scrapy.Field()      # 书名
    book_cover = scrapy.Field()     # 封面图片
    detail_link = scrapy.Field()    # 详情页连接
    author = scrapy.Field()         # 作者
    publisher = scrapy.Field()      # 出版社
    pub_data = scrapy.Field()       # 出版时间
    price = scrapy.Field()          # 书籍价格

