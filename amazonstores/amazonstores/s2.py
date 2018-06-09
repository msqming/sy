#!/usr/bin/python
# -*- coding:utf-8 -*-
import pymysql

def reddata():
    # 创建连接
    conn = pymysql.connect(host='119.23.52.82', port=3306, user='root', passwd='root123.com', db='amazonstores',charset='utf8')
    # 创建游标
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    # 取数据
    # cursor.execute('select asin,deal_url from stores where reviews > 1 and spider_time = "2018-05-15"')
    cursor.execute('select asin,best_rank,price,score,sold_by,seller_num,reviews from stores where spider_time = "20180608"')

    data1 = cursor.fetchall()

    cursor.execute('select asin,best_rank,price,score,sold_by,seller_num,reviews from stores where spider_time = "20180609"')

    data2 = cursor.fetchall()

    conn.commit()
    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()

    # print(data1)

    return data1,data2


def save_to_file(data1, data2):


    with open('0609.txt', 'w', encoding='utf-8') as f:
        f.write('Holy Stone店铺商品排名增长信息 -- 0609'+'\n')
        f.write('\n')

        data3 = []
        data4 = []

        for item in data1:
            # print(item)
            rank = item['best_rank'].strip()[1:].replace('#','')
            if rank.isdigit() and int(rank) < 5000:
                # print(rank,item['asin'])
                data3.append(item)


        for item in data2:
            # print(item)
            rank = item['best_rank'].strip()[1:].replace('#', '')
            if rank.isdigit() and int(rank) < 5000:
                # print(rank, item['asin'])
                data4.append(item)

        for i in data4:
            for j in data3:
                if i['asin'] == j['asin']:
                    f.write('asin码:{0}  price:{1}  评分:{2}'.format(i['asin'], i['price'], i['score']) + '\n')
                    f.write('卖家: {0} 其他卖家数量：{1}'.format(i['sold_by'], i['seller_num']) + '\n')
                    f.write('今天reviews:{0}  昨天reviews:{1}  增长数量：{2}'.format(i['reviews'],j['reviews'],int(i['reviews'])-int(j['reviews'])) +'\n')
                    f.write('现在排名：{0} 昨天排名：{1}'.format(i['best_rank'].strip()[1:], j['best_rank'].strip()[1:])+'\n')
                    f.write('增长排名：{0}'.format(int(j['best_rank'].strip()[1:])-int(i['best_rank'].strip()[1:]))+'\n')
                    f.write('\n')


if __name__ == '__main__':
    data1,data2 = reddata()
    save_to_file(data1,data2)

