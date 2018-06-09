# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from pyquery import PyQuery as pq
from ..items import AmazontoysItem
import re
import time
import json


class ToysSpider(Spider):
    name = 'toys'
    allowed_domains = ['www.amazon.com']
    start_urls = ['https://www.amazon.com/']

    def start_requests(self):
        start_url1 = 'https://www.amazon.com/Best-Sellers-Toys-Games/zgbs/toys-and-games/ref=zg_bs_nav_0'
        start_url2 = 'https://www.amazon.com/gp/new-releases/toys-and-games/ref=zg_bsnr_nav_0'
        start_url3 = 'https://www.amazon.com/gp/most-wished-for/toys-and-games/ref=zg_mw_nav_0'
        start_url4 = 'https://www.amazon.com/gp/most-gifted/toys-and-games/ref=zg_mg_nav_0'

        for start_url in [start_url1,start_url2,start_url3,start_url4]:
        # for start_url in [start_url1]:
            yield Request(url=start_url,callback=self.parse_comm_list)

    def parse_comm_list(self, response):
        """解析商品列表"""
        doc = pq(response.text)
        fenlei = re.search('https.*?(Best-Sellers|most-wished-for|most-gifted|new-releases).*?_0', response.url)
        if fenlei:
            fenlei = fenlei.group(1)

        leibie1 = doc('#zg_browseRoot span.zg_selected')
        if leibie1:
            leibie1 = leibie1.text()

        # 获取当前页面的jaxURL
        list_url = response.url.split('/ref=')[0]
        for i in range(1, 6):
            page_url = list_url + '?_encoding=UTF8&pg={0}&ajax=1'.format(i)
            yield Request(url=page_url, callback=self.parse_comm_info,
                          meta={'fenlei': fenlei,'leibie':leibie1})
            time.sleep(3)

        # 页面中左侧的所有a标签
        li_tag = doc('#zg_browseRoot > ul > ul > li')

        # 获取左侧页面的URL
        for a_tag in li_tag.items():
            leibie2 = a_tag('a').text()
            comm_url = a_tag('a').attr('href')

            list_url = comm_url.split('/ref=')[0]

            for i in range(1, 6):
                yield Request(url=list_url + '?_encoding=UTF8&pg={0}&ajax=1'.format(i), callback=self.parse_comm_info,
                              meta={'leibie': leibie1 + '>' + leibie2, 'fenlei': fenlei})
                time.sleep(3)

            # 获取第二层URL
            yield Request(url=list_url, callback=self.parse_comm_list2,dont_filter=True,
                          meta={'leibie': leibie1+'>'+leibie2,'fenlei': fenlei})
            time.sleep(2)

    def parse_comm_list2(self, response):
        """第二层URL商品列表"""
        fenlei = response.meta['fenlei']
        leibie2 = response.meta['leibie']

        doc = pq(response.text)

        # 页面中左侧的所有a标签
        li_tag = doc('#zg_browseRoot > ul > ul > ul > li')

        # 获取左侧页面的URL
        for a_tag in li_tag.items():
            leibie3 = a_tag('a').text()
            comm_url = a_tag('a').attr('href')

            list_url = comm_url.split('/ref=')[0]

            for i in range(1, 6):
                yield Request(url=list_url + '?_encoding=UTF8&pg={0}&ajax=1'.format(i), callback=self.parse_comm_info,
                              meta={'leibie': leibie2 + '>' + leibie3, 'fenlei': fenlei}, dont_filter=True)
                time.sleep(3)

            # 获取第三层URL
            yield Request(url=list_url, callback=self.parse_comm_list3,
                          meta={'leibie': leibie2 + '>' + leibie3, 'fenlei': fenlei})
            time.sleep(2)

    def parse_comm_list3(self, response):
        """第三层URL商品列表"""
        fenlei = response.meta['fenlei']
        leibie3 = response.meta['leibie']
        doc = pq(response.text)

        # 页面中左侧的所有a标签
        li_tag = doc('#zg_browseRoot > ul > ul > ul > ul > li')
        # 获取左侧页面的URL
        for a_tag in li_tag.items():
            leibie4 = a_tag('a').text()
            comm_url = a_tag('a').attr('href')

            list_url = comm_url.split('/ref=')[0]

            for i in range(1, 6):

                yield Request(url=list_url + '?_encoding=UTF8&pg={0}&ajax=1'.format(i), callback=self.parse_comm_info,
                              meta={'leibie': leibie3 + '>' + leibie4, 'fenlei': fenlei}, dont_filter=True)
                time.sleep(3)

    def parse_comm_info(self, response):
        """解析单个商品信息"""
        doc = pq(response.text)
        comm_list = doc('div.zg_itemImmersion').items()

        for comm in comm_list:
            # 排名
            rank_num = comm('div.zg_rankDiv > span.zg_rankNumber').text()

            # asin码
            asin = comm('div.zg_itemWrapper > div.a-section.a-spacing-none.p13n-asin').attr('data-p13n-asin-metadata')
            if asin:
                asin = json.loads(asin)['asin']

            # 商品详情页URL
            deal_url = comm('div.zg_itemWrapper > div.a-section.a-spacing-none.p13n-asin > a.a-link-normal').attr('href')
            if deal_url:
                deal_url = 'https://www.amazon.com' + deal_url

            # 商品标题
            comm_title = comm('div.zg_itemWrapper div.p13n-sc-truncate.p13n-sc-line-clamp-2')
            # div > a > div.p13n-sc-truncate.p13n-sc-line-clamp-2
            if comm_title:
                comm_title = str(comm_title.text())

            # 商品的综合评分
            score = comm('div.a-icon-row.a-spacing-none > a.a-link-normal').attr('title')
            if score:
                score = score.split()[0]
            else:
                score = 0

            # 商品的评分人数
            reviews = comm('div.a-icon-row.a-spacing-none > a.a-size-small.a-link-normal')
            if reviews:
                reviews = reviews.text().replace(',','')
            else:
                reviews = 0

            # 商品价格
            price = comm('div.a-row span.p13n-sc-price')
            if price:
                price = int(price.text()[1:])
            else:
                price = 0

            result = {
                'fenlei': response.meta['fenlei'],
                'leibie': response.meta['leibie'],
                'rank_num': rank_num,
                'asin': asin,
                'deal_url': deal_url,
                'comm_title': comm_title,
                'score': score,
                'reviews': reviews,
                'price': price,
            }
            # print(result)
            # print()

            yield Request(url=deal_url, callback=self.parse_comm_deal, dont_filter=True,
                          meta={'result':result}
                          )
            time.sleep(2)

    def parse_comm_deal(self, response):
        """解析商品的详细信息"""
        doc = pq(response.text)
        # 卖家
        sold_by = doc('#merchant-info').text()
        if sold_by:
            sold_by = sold_by.strip().split('.')[0]
        else:
            sold_by = 'Amazon'
        # 卖家数量
        seller_num = doc('#olp_feature_div > div > span:nth-child(1) > a').text()
        if seller_num:
            seller_num1 = re.search('(New|new) \((\d+)\) from',seller_num,re.S)
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
                rank = rank.group(1).replace(',','')
            else:
                rank = 'none'

        response.meta['result']['sold_by'] = sold_by
        response.meta['result']['seller_num'] = seller_num
        response.meta['result']['rank'] = rank
        response.meta['result']['spider_time'] = time.strftime('%Y%m%d')

        # result = {
        #     'asin': response.meta['result']['asin'],
        #     'comm_title': response.meta['result']['comm_title'],
        #     'price': response.meta['result']['price'],
        #     'reviews': response.meta['result']['number'],
        #     'score': response.meta['result']['score'],
        #     'deal_url': response.meta['result']['deal_url'],
        #     'fenlei': response.meta['result']['fenlei'],
        #     'rank_num': response.meta['rank_num'],
        #
        # }
        # print(result)

        item = AmazontoysItem()
        for field in item.fields:
            # print(field)
            if field in response.meta['result'].keys():
                item[field] = response.meta['result'].get(field)

        yield item
