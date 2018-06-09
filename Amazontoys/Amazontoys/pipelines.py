# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


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

        self.cursor.execute('insert into Toys(asin,reviews,price,score,rank,sold_by,seller_num,rank_num,fenlei,deal_url,comm_title,spider_time,leibie) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                            (item['asin'], item['reviews'],
                            item['price'], item['score'],
                            item['rank'], item['sold_by'],
                            item['seller_num'], item['rank_num'],
                            item['fenlei'], item['deal_url'],
                            item['comm_title'], item['spider_time'],
                            item['leibie']
                            ))
        self.conn.commit()

        print(item['rank_num'], '存储成功')
        return item

    def close_spider(self,spider):
        # 关闭数据库
        self.cursor.close()
        self.conn.close()
