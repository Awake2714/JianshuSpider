# -*- coding: utf-8 -*-
import scrapy
import re
from Jianshu.items import JianshuItem
from Jianshu.settings import ARTICLE_ID

class JianshuSpider(scrapy.Spider):
    name = "jianshu"
    allowed_domains = ["jianshu.com"]
    start_urls = ['http://jianshu.com/']
    base_url = 'https://www.jianshu.com/p/{}'

    def start_requests(self):
        url = self.base_url.format(ARTICLE_ID)
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        title = response.xpath('//h1/text()').extract_first()
        publish_time = response.xpath('//time[1]/text()').extract_first().replace('.', '/')
        words = re.search('<span>字数 (\d+?)</span>', response.text).group(1)
        views = re.search('<span>阅读 (\d+?)</span>', response.text).group(1)
        like = re.search('aria-label="查看点赞列表">(\d+?)<!-- -->赞</span>', response.text)
        if like:
            likes = like.group(1)
        else:
            likes = 0
        dislikes = re.search('"downvotes_count":(\d+),', response.text).group(1)
        author = re.search('"nickname":"(.*?)"', response.text, re.S).group(1)
        url = response.url
        item = JianshuItem(title=title, publish_time=publish_time, words=words, views=views, url=url,
                           likes=likes, dislikes=dislikes, author=author)
        recommends = response.xpath('//ul/li/div/div[1]/a/@href').extract()
        for recommend in recommends:
            recommend = response.urljoin(recommend)
            yield scrapy.Request(url=recommend, callback=self.parse)
        yield item