# JianshuSpider
简书全网爬虫
+ 基于scrapy框架，从热门文章入手，获取文章标题，链接，作者，字数，阅读量，点赞数，不喜欢数，发布时间，将数据保存到mongodb数据库
+  提取推荐阅读文章链接，对简书进行全网爬虫
## jianshu.py
发起请求，解析网页
## items.py
要保存的字段
## setting.py
配置文件
## pipeline.py
存储数据
