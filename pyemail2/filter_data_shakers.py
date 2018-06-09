#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pymysql
import re


def conn_mysql():
    # 创建连接
    conn = pymysql.connect(host='119.23.52.82', port=3306, user='root', passwd='root123.com', db='amazonshakers',
                           charset='utf8')

    # 创建游标
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    # 取数据
    cursor.execute('select * from toyshakers where reviews < 101 and price < 100 and spider_time = "20180609"')

    data = cursor.fetchall()

    conn.commit()
    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()

    return data


def save_to_file(data):
    with open('20180609.txt','w',encoding='utf-8') as f:

        f.write('2018年6月9日，亚马逊商品在Toys类排名上升前10的商品' + '\n')
        f.write('说明：以下商品是从排名上升中去除了评论数或价格大于100的' + '\n')
        f.write('\n')
        for item in data:

            b = re.search('Sales rank: (.*?) \((previously unranked|was(.*?))\)', item['sales_rank'])

            # if item['seller_num']:
            #     seller_num1 = re.search('(New|new) \((\d+)\) from', item['seller_num'], re.S)
            #     if seller_num1:
            #         seller_num = seller_num1.group(2)
            #     else:
            #         seller_num = item['seller_num'].split()[0]
            # else:
            #     seller_num = 1
            f.write(' 商品名称: {} '.format(item['comm_title'])+'\n')
            f.write(' 商品ASIN码 {}'.format(item['asin'])+'\n')
            f.write(' 商品地址: {}'.format(item['deal_url'])+'\n')
            f.write(' reviews：{0}   价格：{1},'.format(item['reviews'],item['price'])+'\n')
            # f.write(' 原排名{0},  现在排名{1},  增长率为{2},  卖家数量 {3}'.format(b.group(2).split()[1],b.group(1),item['percent'],seller_num)+'\n')
            f.write(' 昨天排名{0},  现在排名{1},  增长率为{2}'.format(item['sales_rank'].split()[4][:-1],item['sales_rank'].split()[2], item['rise'])+'\n')
            f.write('\n')


def main():
    data = conn_mysql()
    if data:
        save_to_file(data)


if __name__ == '__main__':
    main()