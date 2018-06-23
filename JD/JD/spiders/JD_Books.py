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
            print(big_category)
