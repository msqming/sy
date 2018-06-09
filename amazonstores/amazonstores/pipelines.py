# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
import pymongo


class MysqlPipeline(object):

    def __init__(self,HOST,PORT,USER,PASSWD,MYSQL_DB):
        self.HOST = HOST
        self.PORT = PORT
        self.USER = USER
        self.PASSWD = PASSWD
        self.MYSQL_DB = MYSQL_DB

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            HOST=crawler.settings.get('HOST'),
            PORT=crawler.settings.get('PORT'),
            USER=crawler.settings.get('USER'),
            PASSWD=crawler.settings.get('PASSWD'),
            MYSQL_DB=crawler.settings.get('MYSQL_DB'),
        )

    def open_spider(self,spider):
        # 连接MYSQL数据库
        self.conn = pymysql.connect(host=self.HOST,port=self.PORT,user=self.USER,passwd=self.PASSWD,db=self.MYSQL_DB,charset='utf8')
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        # 把数据库写入MYSQL数据库

        self.cursor.execute('insert into stores(asin,reviews,price,score,best_rank,answered,sold_by,seller_num,brand,label,spider_time,deal_url,comm_title) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                            (item['asin'], item['reviews'],
                            item['price'], item['score'],
                            item['best_rank'], item['answered'],
                            item['sold_by'], item['seller_num'],
                            item['brand'], item['label'],
                            item['spider_time'], item['deal_url'],
                            item['comm_title']
                            ))
        self.conn.commit()

        print(item['asin'], '存储成功')
        return item

    def close_spider(self,spider):
        # 关闭数据库
        self.cursor.close()
        self.conn.close()


class MongoPipeline(object):

    def __init__(self,mongo_uri,mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self,spider):
        # 连接mongo数据库
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        # 把数据库写入mongodb数据库

        self.db['stores'].insert(dict(item))
        return item

    def close_spider(self,spider):
        # 关闭数据库
        self.client.close()


