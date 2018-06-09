# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from pyquery import PyQuery as pq
from selenium import webdriver
import re


class SmSpider(Spider):
    name = 'sm'
    # allowed_domains = ['www.amazon.com']
    # start_urls = ['https://www.amazon.com/']

    def __init__(self):
        self.browser = webdriver.Chrome()
        self.browser.set_page_load_timeout(10)

    def closed(self, spider):
        print('spider closed')
        self.browser.close()

    def start_requests(self):
        start1_url = 'https://www.amazon.co.uk/s?marketplaceID=A1F83G8C2ARO7P&me=A14DB0COW8CC7&merchant=A14DB0COW8CC7&redirect=true'

        yield Request(url=start1_url,callback=self.parse_comm)

    def parse_comm(self, response):
        """解析商品列表"""
        doc = pq(response.text)

        comm_list = doc('#s-results-list-atf > li.s-result-item.s-result-card-for-container-noborder.s-carded-grid.celwidget').items()

        for item in comm_list:
            asin = item('li').attr('data-asin')
            comm_title = item('li div.a-row.a-spacing-mini a.a-link-normal.s-access-detail-page.s-color-twister-title-link.a-text-normal').attr('title')
            deal_url = item('li div.a-row.a-spacing-mini a.a-link-normal.s-access-detail-page.s-color-twister-title-link.a-text-normal').attr('href')

            # print(asin)
            # print(deal_url)
            # print()

            yield Request(url=deal_url, callback=self.parse_deal, meta={'asin':asin})

    def parse_deal(self, response):
        asin = response.meta['asin']
        doc = pq(response.text)
        # 排名
        best_rank = doc(
            '#prodDetails div.a-row.a-spacing-top-base > div.a-column.a-span6 > div.a-row.a-spacing-base').text()
        if best_rank:
            best_rank = re.search('Best Sellers Rank(.*?)in Toys & Games', best_rank, re.S)
            if best_rank:
                best_rank = best_rank.group(1).replace(',', '')
            else:
                best_rank = 'none'

        print(best_rank)