# -*- coding: utf-8 -*-
from scrapy import Spider, Request
import pymysql
import time
from pyquery import PyQuery as pq


class CommentSpider(Spider):
    name = 'comment'
    allowed_domains = ['www.amazon.com']
    start_urls = ['http://www.amazon.com/']

    def __init__(self):

        # 创建连接
        conn = pymysql.connect(host='119.23.52.82', port=3306, user='root', passwd='root123.com', db='amazonstores',
                               charset='utf8')
        # 创建游标
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        # 取数据
        cursor.execute('select asin,deal_url from stores where reviews > 1 and spider_time = "2018-05-15"')

        self.data = cursor.fetchall()
        # print(self.data)
        # print()

        conn.commit()
        # 关闭游标
        cursor.close()
        # 关闭连接
        conn.close()

    def start_requests(self):
        for data in self.data:
            # print(data['asin'],data['deal_url'])
            comm_url = data['deal_url']
            if not comm_url.endswith:
                comm_url = comm_url + '/#customerReviews'
            else:
                comm_url = comm_url + '#customerReviews'
            yield Request(url=comm_url,callback=self.parse,meta={'asin':data['asin']})
            time.sleep(2)

    def parse(self, response):
        # print(response.meta['asin'])
        # print(response.url)
        doc = pq(response.text)
        reviews_url = doc('#dp-summary-see-all-reviews').attr('href')
        if reviews_url:
            reviews_url = 'https://www.amazon.com'+reviews_url
        # print(reviews_url)

        yield Request(url=reviews_url,callback=self.parse2)

    def parse2(self,response):

        doc = (response.text)

        reviews_list = doc('#cm_cr-review_list div.a-section.review')
        print(reviews_list)
        print()

        # for item in reviews_list:
        #     print(item('div.a-section.celwidget').attr('id'))

