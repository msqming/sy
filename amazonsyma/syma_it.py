#!/usr/bin/python
# -*- coding:utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pyquery import PyQuery as pq
import time
import requests
import random
import re
import pymysql
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

HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': random.choice(UA_LIST)
}

browser = webdriver.Chrome()
wait = WebDriverWait(browser,10)


def get_index():
    start_url = 'https://www.amazon.it/s?marketplaceID=APJ6JRA9NG5V4&me=A2OS6VL69WFV70&merchant=A2OS6VL69WFV70&redirect=true'

    try:
        browser.get(start_url)

        browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(3)
        data1 = parse_index(browser.page_source)

        # # 跳转下一页
        # next_page = wait.until(
        #     EC.element_to_be_clickable((By.CSS_SELECTOR,'#pagnNextString'))
        # )
        # next_page.click()
        # browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        # time.sleep(3)
        # data2 = parse_index(browser.page_source)

        print(len(data1))
        if data1:
            browser.close()

        return data1

    except TimeoutException:
        return get_index()

    # return browser.page_source,browser


def parse_index(html):
    doc = pq(html)
    comm_list = doc('#s-results-list-atf > li.s-result-item.s-result-card-for-container-noborder.s-carded-grid.celwidget').items()

    data = []
    for item in comm_list:
        asin = item('li').attr('data-asin')
        comm_title = item('li div.a-row.a-spacing-mini a.a-link-normal.s-access-detail-page.s-color-twister-title-link.a-text-normal').attr('title')
        deal_url = item('li div.a-row.a-spacing-mini a.a-link-normal.s-access-detail-page.s-color-twister-title-link.a-text-normal').attr('href')
        score = item('li div.a-row.a-spacing-none span.a-icon-alt').text()
        if score:
            # score = score
            if 'Prime' in score and len(score) > 5:
                score = score.split()[1]
            else:
                score = score.split()[0]
        else:
            score = 0

        reviews = item('li div.a-row.a-spacing-none a.a-size-small.a-link-normal.a-text-normal').text()
        if reviews:
            reviews = reviews
            # reviews = reviews.split()[-1]
        else:
            reviews = 0

        result = {
            'asin': asin,
            'score': score,
            'reviews': reviews,
            'comm_title': comm_title,
            'deal_url': deal_url,
            'site': 'it'
        }

        data.append(result)

    return data


def get_deal(item):

    try:
        response = requests.get(url=item['deal_url'], headers=HEADERS,)
        # print(response)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException as e:
        get_index(item)
        print(e)



def parse_deal(deal_html,result):
    doc = pq(deal_html)
    # 排名
    # prodDetails column.col2
    best_rank = doc('#prodDetails > div.wrapper.ITlocale > div.column.col2').text()
    if best_rank:
        best_rank = re.search('Bestseller di Amazon(.*?)Top 100\)', best_rank, re.S)
        if best_rank:
            best_rank = best_rank.group(1).replace(',', '').strip().split()[1].replace('.','')
        else:
            best_rank = 0

    result['best_rank'] = best_rank
    result['spider_time'] = time.strftime('%Y%m%d')

    return result


def conn_mysql():
    # 创建连接
    conn = pymysql.connect(host='119.23.52.82', port=3306, user='root', passwd='root123.com', db='amazon_syma',charset='utf8')

    return conn


def save_to_mysql(conn,result):
    # 创建游标
    cursor = conn.cursor()

    # 一次性插入多条数据
    try:
        cursor.execute('insert into syma(asin,score,reviews,best_rank,spider_time,site,comm_title) values(%s,%s,%s,%s,%s,%s,%s)',
                           (result['asin'],result['score'],
                            result['reviews'],result['best_rank'],
                            result['spider_time'],
                            result['site'],result['comm_title'],
                            ))
        print(result['asin'],'存储成功')
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
    data1 = get_index()
    for data in [data1]:
        for item in data:
            deal_html = get_deal(item)
            if deal_html:
                result = parse_deal(deal_html, item)
                # print(result)
                conn = conn_mysql()
                if conn:
                    save_to_mysql(conn, result)
            time.sleep(3)


if __name__ == '__main__':

    main()