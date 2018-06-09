#! /usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Ypp

import requests
import random
import time
import re
import json
import pymysql
from pyquery import PyQuery as pq
from requests.exceptions import RequestException

UA_LIST = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Mozilla/5.0 (compatible; Baiduspider/2.0; - +http://www.baidu.com/search/spider.html)',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
        'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
        'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)',
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',

]
PROXIES_LIST = [
    'https://222.221.147.15:56591'
    'https://112.87.84.6:56915'
    'https://111.76.65.131:51863'
    'https://42.243.3.138:56591'
    'https://101.205.55.193:57135'

]
proxies = {'http': random.choice(PROXIES_LIST)}

HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'www.amazon.com',
    'User-Agent': random.choice(UA_LIST)
}


def get_index(url):
    """获取网页html代码"""
    try:
        response = requests.get(url=url,headers=HEADERS)
        print(response)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException as e:
        get_index(url)
        print(e)


def parse_index(html):
    """解析网页源代码"""
    doc = pq(html)
    comm_list = doc('div.zg_itemImmersion').items()
    for comm in comm_list:
        # print(comm)
        # 排名
        ranknumber = comm('div.zg_rankDiv > span.zg_rankNumber').text()
        if ranknumber:
            ranknumber = ranknumber.replace('.','')
            # print(ranknumber)
        # 上升排名
        sales_rank = comm('div.a-row.a-spacing-small > span.zg_salesMovement').text()
        if sales_rank:
            sales_rank = sales_rank
            # print(sales_rank)
        # 上升率
        percent = comm('div.a-row.a-spacing-small span.zg_percentChange').text()
        if percent:
            percent = percent.replace(',','')
        else:
            percent = 'null'

        # # 商品标题
        # comm_title = comm('div.zg_itemWrapper div.p13n-sc-truncate.p13n-sc-line-clamp-2')
        # # div > a > div.p13n-sc-truncate.p13n-sc-line-clamp-2
        # if comm_title:
        #     comm_title = comm_title.text()

        # 商品详情页URL
        deal_url = comm('div.zg_itemWrapper > div.a-section.a-spacing-none.p13n-asin > a.a-link-normal').attr('href')
        if deal_url:
            deal_url = 'https://www.amazon.com' + deal_url
        # asin
        # asin = re.search('https.*?dp/(.*?)?/ref',deal_url)
        # if asin:
        #     asin = asin.group(1)
        asin = comm('div.zg_itemWrapper > div.a-section.a-spacing-none.p13n-asin').attr('data-p13n-asin-metadata')
        if asin:
            asin = json.loads(asin)['asin']
        # 商品的综合评分
        score = comm('div.a-icon-row.a-spacing-none > a.a-link-normal').attr('title')
        if score:
            score = score.split()[0]
        else:
            score = 0

        # 商品的评分人数
        reviews = comm('div.a-icon-row.a-spacing-none > a.a-size-small.a-link-normal')
        if reviews:
            reviews = int(reviews.text().replace(',', ''))
        else:
            reviews = 0

        # 商品价格
        price = comm('div.a-row span.p13n-sc-price')
        if price:
            price = price.text()[1:]
        else:
            price = 0

        result = {
            'asin':asin,
            'percent':percent,
            'ranknumber':ranknumber,
            'sales_rank':sales_rank,
            'deal_url':deal_url,
            'price':price,
            'reviews':reviews,
            'score':score,
            # 'comm_title':comm_title,
        }
        # print(result)
        # return result
        deal_html = get_deal_info(deal_url)
        if deal_html:
            data = parse_deal_info(deal_html, result)
            # print(data)
            if data:
                conn = conn_mysql()
                if conn:
                    save_to_mysql(conn, data)
        time.sleep(2)


def get_deal_info(deal_url):
    """获取详情页html代码"""
    try:
        response = requests.get(url=deal_url, headers=HEADERS, proxies=proxies)
        print(response)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException as e:
        print(e)
        time.sleep(8)
        get_deal_info(deal_url)


def parse_deal_info(html, result):
    """解析详情页html代码"""
    doc = pq(html)

    # 商品标题
    comm_title = doc('#productTitle').text()
    if comm_title:
        comm_title = comm_title.strip()

    # 卖家数量
    seller_num = doc('#olp_feature_div > div > span:nth-child(1) > a').text()
    if seller_num:
        seller_num = seller_num
    else:
        seller_num = 1

    # 卖家
    sold_by = doc('#merchant-info').text()
    if sold_by:
        sold_by = sold_by.split('.')[0]
    else:
        sold_by = 'Amazon'

    result['comm_title'] = comm_title
    result['seller_num'] = seller_num
    result['sold_by'] = sold_by
    result['spider_time'] = time.strftime('%Y%m%d')

    # print(result)
    return result


def conn_mysql():
    # 创建连接
    conn = pymysql.connect(host='119.23.52.82', port=3306, user='root', passwd='root123.com', db='amazonshakers',
                           charset='utf8')

    return conn


def save_to_mysql(conn,result):
    # 创建游标
    cursor = conn.cursor()

    # 一次性插入多条数据
    try:
        cursor.execute('insert into toyshakers(asin,reviews,price,score,rise,seller_num,sold_by,sales_rank,ranknumber,spider_time,deal_url,comm_title) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                           (result['asin'],result['reviews'],
                            result['price'], result['score'],
                            result['percent'], result['seller_num'],
                            result['sold_by'],result['sales_rank'],
                            result['ranknumber'],result['spider_time'],
                            result['deal_url'],result['comm_title']
                            ))
        print(result['ranknumber'],result['asin'],'存储成功')
    except Exception as e:
        print(result['asin'], '存储失败')
        print(e)

    # 提交,不然无法保存新建或者修改的数据
    conn.commit()

    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()


def main():
    start_url1 = 'https://www.amazon.com/gp/movers-and-shakers/toys-and-games/ref=zg_bsms_pg_1?ie=UTF8&pg=1&ajax=1'
    start_url2 = 'https://www.amazon.com/gp/movers-and-shakers/toys-and-games/ref=zg_bsms_pg_2?ie=UTF8&pg=2&ajax=1'
    start_url3 = 'https://www.amazon.com/gp/movers-and-shakers/toys-and-games/ref=zg_bsms_pg_3?ie=UTF8&pg=3&ajax=1'
    start_url4 = 'https://www.amazon.com/gp/movers-and-shakers/toys-and-games/ref=zg_bsms_pg_4?ie=UTF8&pg=4&ajax=1'
    start_url5 = 'https://www.amazon.com/gp/movers-and-shakers/toys-and-games/ref=zg_bsms_pg_5?ie=UTF8&pg=5&ajax=1'

    for start_url in [start_url1,start_url2,start_url3,start_url4,start_url5]:
    # for start_url in [start_url1]:
        html = get_index(start_url)
        if html:
            parse_index(html)

        time.sleep(10)


if __name__ == '__main__':
    main()
