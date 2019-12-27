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
        t = int(re.search(r'"first_shared_at":(\d+?),', response.text).group(1))  #时间戳
        publish_time = str(datetime.fromtimestamp(t))    #发布时间
        words = re.search(r'"wordage":(\d+?),"featured_comments_count"', response.text).group(1)    #字数
        views = re.search(r'"views_count":(\d+?),"notebook_id"', response.text).group(1)    #阅读数
        like = re.search(r'aria-label="查看点赞列表">(\d+?)<!-- -->赞', response.text)     #点赞数
        if like:
            likes = like.group(1)
        else:
            likes = 0
        dislikes = re.search(r'"downvotes_count":(\d+),', response.text).group(1)   #不喜欢数
        author = re.search('"nickname":"(.*?)"', response.text, re.S).group(1)      #作者
        url = response.url      #文章链接
        item = JianshuItem(title=title, publish_time=publish_time, words=words, views=views, url=url,
                           likes=likes, dislikes=dislikes, author=author)
        recommends = response.xpath('//ul/li/div/div[1]/a/@href').extract()
        for recommend in recommends:
            recommend = response.urljoin(recommend)
            yield scrapy.Request(url=recommend, callback=self.parse)
        yield item
