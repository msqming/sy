#!/usr/bin/python
# -*- coding:utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pyquery import PyQuery as pq
import time
import re


def get_index():
    browser = webdriver.Chrome()
    wait = WebDriverWait(browser,5)
    try:
        browser.get('https://www.amazon.com/s?marketplaceID=ATVPDKIKX0DER&me=A3QTILSGJZUURE&merchant=A3QTILSGJZUURE&redirect=true')
        for i in range(6):
            browser.execute_script("window.scrollTo(0,10000)")
            html = browser.page_source
            get_products(html)
            next_page = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#pagnNextString')))
            next_page.click()
            time.sleep(5)
        return browser

    except TimeoutError:
        print('Time out')


def get_products(html):
    doc = pq(html)
    items = doc('#s-results-list-atf li.s-result-item.celwidget').items()
    for item in items:
        num = item('li.s-result-item.celwidget').attr('data-result-rank')
        asin = item('li.s-result-item.celwidget').attr('data-asin')
        # comm_title = item('div.a-row.a-spacing-none.sx-line-clamp-4 > a').attr('title')
        comm_title = item('div.a-row.a-spacing-mini a.a-link-normal.s-access-detail-page.s-color-twister-title-link.a-text-normal').attr('title')
        comm_url = item('div.a-row.a-spacing-mini a.a-link-normal.s-access-detail-page.s-color-twister-title-link.a-text-normal').attr('href')
        price = item('div.a-row.a-spacing-none span.a-offscreen')
        if price:
            price = price.text().split()[-1][1:]
        else:
            price = 0
        reviews = item('div.a-row.a-spacing-none a.a-size-small.a-link-normal.a-text-normal')
        if reviews:
            reviews = reviews.text().split()[-1].replace(',','')
        else:
            reviews = 0
        score = item('span.a-icon-alt').text()
        if score and 'out' in score:
            score = score.split()[1]
        else:
            score = 0
        result = {
            'num': num,
            'asin': asin,
            'comm_title': comm_title,
            'comm_url': comm_url,
            'price': price,
            'reviews': reviews,
            'score': score,

        }
        # print(result)
        # print()
        get_dealinfo(result)


def get_dealinfo(result):
    browser = webdriver.Chrome()
    # wait = WebDriverWait(browser, 5)
    try:
        browser.get(result['comm_url'])
        # browser.execute_script("window.scrollTo(0,2000)")
        time.sleep(3)
        html = browser.page_source
        parser_dealinfo(html,browser,result)

    except TimeoutError:
        print('Time out')


def parser_dealinfo(html,browser,result):

    doc = pq(html)
    # sold_by = doc('#merchant-info').text()
    #
    # seller_num = doc('#olp_feature_div > div').text()
    #
    # rank = doc('#prodDetails').text()
    # 卖家
    sold_by = doc('#merchant-info').text()
    if sold_by:
        sold_by = sold_by.strip().split('.')[0]
    else:
        sold_by = 'Amazon'
    # 卖家数量
    seller_num = doc('#olp_feature_div > div > span:nth-child(1) > a').text()
    if seller_num:
        seller_num1 = re.search('(New|new) \((\d+)\) from', seller_num, re.S)
        if seller_num1:
            seller_num = seller_num1.group(2)
        else:
            seller_num = seller_num.split()[0]
    else:
        seller_num = 1

    rank = doc('#prodDetails div.a-row.a-spacing-top-base > div.a-column.a-span6 > div.a-row.a-spacing-base').text()
    if rank:
        rank = re.search('Best Sellers Rank(.*?)in Toys & Games', rank, re.S)
        if rank:
            rank = rank.group(1).replace(',', '').strip().replace('#','')
        else:
            rank = 'none'

    # print(sold_by,seller_num)
    # print(rank)
    # print()
    result['sold_by'] = sold_by
    result['seller_num'] = seller_num
    result['rank'] = rank

    browser.close()

    if int(rank) < 5000:
        save_to_file(result)


def save_to_file(result):
    with open('0528.txt','a+',encoding='utf-8') as f:
        f.write('Holy Stone店铺商品排名增长信息0528\n')
        f.write('asin码: {0}  price: {1}  评分: {2}'.format(result['asin'],result['price'],result['score'])+'\n')
        f.write('卖家: {0} 其他卖家数量：{1}'.format(result['sold_by'],result['seller_num'])+'\n')
        f.write('reviews增长数量：{0} 增长排名：{1}'.format(result['reviews'],result['rank'])+'\n')


if __name__ == '__main__':
    browser = get_index()

    browser.close()