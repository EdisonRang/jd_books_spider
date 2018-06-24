# -*- coding: utf-8 -*-
import json
import scrapy
from JD.items import JdItem
# 1.导数爬虫类
from scrapy_redis.spiders import RedisSpider

# 2.修改继承类
class JdBooksSpider(RedisSpider):
    # 3.注销起始url和允许的域
    # name = 'JD_Books'
    # allowed_domains = ['jd.com']
    # # 修改起始URL
    # start_urls = ['https://book.jd.com/booksort.html']

    # 4.动态获取允许域
    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        # 需要强转成列表
        self.allowed_domains = list(filter(None, domain.split(',')))
        # 需要修改类
        super(JdBooksSpider, self).__init__(*args, **kwargs)

    # 5.设置redis_key
    redis_key = "JD"

    def parse(self, response):
        # 获取大分类节点列表
        big_list = response.xpath('//*[@id="booksort"]/div[2]/dl/dt/a')
        # 遍历列表获取信息
        for big in big_list:
            big_category = big.xpath('./text()').extract_first()
            big_category_link = "https:" + big.xpath('./@href').extract_first()
            # 获取小分类节点列表
            small_list = response.xpath('//*[@id="booksort"]/div[2]/dl/dd[1]/em/a')
            # 遍历列表
            for small in small_list:
                small_category = small.xpath('./text()').extract_first()
                small_category_link = "https:" + small.xpath('./@href').extract_first()
                data ={}
                data['big_category'] = big_category
                data['big_category_link'] = big_category_link
                data['small_category'] = small_category
                data['small_category_link'] = small_category_link
                yield scrapy.Request(
                    url=data['small_category_link'],
                    callback=self.parse_detail,
                    meta={"meta_1":data}
                )

    def parse_detail(self, response):
        data = response.request.meta['meta_1']
        # 获取所有图书节点列表
        books = response.xpath('//*[@id="plist"]/ul/li/div')
        # 创建item对象
        item = JdItem()
        # 遍历节点
        for book in books:
            item['big_category'] = data['big_category']
            item['big_category_link'] = data['big_category_link']
            item['small_category'] = data['small_category']
            item['small_category_link'] = data['small_category_link']

            item['book_name'] = book.xpath('./div[3]/a/em/text()').extract_first()
            item['book_cover'] = book.xpath('./div[1]/a/img/@src|./div[1]/a/img/@data-lazy-img').extract_first()
            try:
                item['detail_link'] = 'https:' + book.xpath('./div[1]/a/@href').extract_first()
            except:
                item['detail_link'] = None
            item['author'] = book.xpath('./div[4]/span[1]/span/a/text()').extract_first()
            item['publisher'] = book.xpath('./div[4]/span[2]/a/text()').extract_first()
            item['pub_data'] = book.xpath('./div[4]/span[3]/text()').extract_first()
            # item['price'] = book.xpath('./div[2]/strong[1]/i/text()').extract_first()
            # yield item
            skuid = book.xpath('./@data-sku').extract_first()
            if skuid != None:
                # 拼接价格url
                price_url = 'https://p.3.cn/prices/mgets?skuIds=J_' + str(skuid)
                yield scrapy.Request(
                url=price_url,
                callback=self.parse_price,
                meta={'meta_2': item}
            )

    def parse_price(self, response):
        item = response.request.meta['meta_2']
        dict_data = json.loads(response.body)
        item['price'] = dict_data[0]['op']
        yield item