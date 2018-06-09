#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pymysql
import re


def conn_mysql():
    # 创建连接
    conn = pymysql.connect(host='119.23.52.82', port=3306, user='root', passwd='root123.com', db='amazon_syma',charset='utf8')

    # 创建游标
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    # 取数据
    cursor.execute('select * from syma where spider_time="20180608" and site="es"')

    data1 = cursor.fetchall()

    cursor.execute('select * from syma where spider_time = "20180609" and site="es"')

    data2 = cursor.fetchall()


    conn.commit()
    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()

    return data1, data2


def save_to_file(data1,data2):
    with open('20180609_es.txt','w',encoding='utf-8') as f:

        f.write('2018年6月9日，syma产品在亚马逊西班牙站的排名' + '\n')
        f.write('说明：增长为正数说明比昨天排名靠后，负数则比昨天排名靠前, 评分显示为“Prime”表示无评分' + '\n')
        f.write('\n')

        for i in data2:
            for j in data1:
                if i['asin'] == j['asin']:

                    f.write(' 商品名称: {0} '.format(i['comm_title']) + '\n')
                    f.write(' 商品ASIN码: {0} 评分:{1}'.format(i['asin'],i['score']) + '\n')
                    f.write(' 站点: {0}'.format(i['site']) + '\n')
                    f.write(' 今天reviews:{0}  昨天reviews:{1}  增长数量：{2}'.format(i['reviews'], j['reviews'],int(i['reviews']) - int(j['reviews'])) + '\n')
                    f.write(' 昨天排名：{0}  今天排名：{1}'.format(j['best_rank'], i['best_rank']) + '\n')
                    f.write(' 增长：{0}'.format(int(i['best_rank'])-int(j['best_rank'])) + '\n')
                    f.write('\n')


def main():
    data1, data2 = conn_mysql()
    if data2:
        save_to_file(data1, data2)


if __name__ == '__main__':
    main()