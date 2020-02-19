# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanItem
import os


# 爬虫操作 解析html
class DoubanSpiderSpider(scrapy.Spider):
    # 爬虫的名称
    name = 'douban_spider'
    # 爬虫允许抓取的域名
    allowed_domains = ['movie.douban.com']
    # 爬虫抓取数据地址,给调度器
    start_urls = ['https://movie.douban.com/top250']
    count = 0

    # 解析列表
    def parse(self, response):
        self.count += 1
        print('count ', self.count)
        items = response.xpath("//ol[@class='grid_view']/li")
        parentPath = './data/'
        if not os.path.exists(parentPath):
            os.makedirs(parentPath)
        for item in items:
            detailUrls = item.xpath(".//div[@class='info']/div[@class='hd']/a/@href").extract()
            if detailUrls:
                print(detailUrls[0])
                yield scrapy.Request(detailUrls[0], callback=self.parse_detail)
                return
        # nextLinks = response.xpath("//div[@class='paginator']//span[@class='next']/a/@href").extract()
        # if nextLinks:
        #     nextLink = self.start_urls[0] + nextLinks[0]
        #     print(nextLink)
        #     yield scrapy.Request(nextLink, callback=self.parse)

    # 解析详情
    def parse_detail(self, response):
        douban_item = DoubanItem()
        douban_item['movie_name'] = response.xpath("//div[@id='content']//h1/span/text()").extract_first()
        douban_item['serial_number'] = response.xpath("//span[@class='top250-no']/text()").extract_first()
        douban_item['star'] = response.xpath("//strong[@class='ll rating_num']/text()").extract_first()
        douban_item['evaluate'] = response.xpath("//a[@class='rating_people']/span/text()").extract_first() + '人评论'
        introduce_ = ''
        introduces = response.xpath("//div[@id='link-report']/span[1]/text()").extract_first()
        for introduce in introduces:
            introduce_ += introduce
        douban_item['introduce'] = introduce_
        douban_item['snapshot'] = response.xpath("//a[@class='nbgnbg']/img/@src").extract_first()
        douban_item['comments'] = response.xpath("//div[@class='comment-item']//span[@class='short']/text()").extract()
        yield douban_item
