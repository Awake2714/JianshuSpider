# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


class JianshuPipeline(object):
    def process_item(self, item, spider):
        return item

class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db, mongo_collection):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_collection = mongo_collection

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri = crawler.settings.get('MONGO_URI'),
            mongo_db = crawler.settings.get('MONGO_DATABASE'),
            mongo_collection = crawler.settings.get('MONGO_COLLECTION')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        self.db[self.mongo_collection].update(
                    {'url': item['url']},
                    {'$set': item},
                    True
                )
        # self.db[self.mongo_collection].insert(item)
        print('save to mongo successfully！', item['url'])
        return item

    def close_spider(self, spider):
        self.client.close()