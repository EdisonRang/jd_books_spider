# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from scrapy.conf import settings


class JdPipeline(object):
    def process_item(self, item, spider):
        return item

class MongoPipeline(object):
    def open_spider(self, spider):
        # 获取数据库配置信息
        host = settings['MONGO_HOST']
        port = settings['MONGO_PORT']
        db = settings['MONGO_DB']
        col = settings['MONGO_COL']
        # 创建数据库连接
        self.client = MongoClient(host, port)
        self.db = self.client[db]
        self.col = self.db[col]

    def process_item(self, item, spider):
        dict_data = dict(item)
        self.col.insert(dict_data)
        return item

    def close_spider(self, spider):
        self.client.close()