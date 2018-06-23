# -*- coding: utf-8 -*-
import scrapy


class JdBooksSpider(scrapy.Spider):
    name = 'JD_Books'
    allowed_domains = ['jd.com']
    # 修改起始URL
    start_urls = ['https://book.jd.com/booksort.html']

    def parse(self, response):
        pass
