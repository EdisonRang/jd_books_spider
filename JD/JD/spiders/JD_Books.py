# -*- coding: utf-8 -*-
import scrapy


class JdBooksSpider(scrapy.Spider):
    name = 'JD_Books'
    allowed_domains = ['jd.com']
    # 修改起始URL
    start_urls = ['https://book.jd.com/booksort.html']

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
                temp ={}
                temp['big_category'] = big_category
                temp['big_category_link'] = big_category_link
                temp['small_category'] = small_category
                temp['small_category_link'] = small_category_link
                yield scrapy.Request(
                    url=temp['small_category_link'],
                    callback=self.parse_detail,
                    meta={"meta_1":temp}
                )

    def parse_detail(self):
        pass

