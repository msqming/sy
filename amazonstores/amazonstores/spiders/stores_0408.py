# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from pyquery import PyQuery as pq
import re
import time
from ..items import AmazonstoresItem


class StoresSpider(Spider):
    name = 'stores0408'
    allowed_domains = ['www.amazon.com']
    start_urls = ['https://www.amazon.com/']

    def start_requests(self):
        # start_url1 = 'https://www.amazon.com/s?marketplaceID=ATVPDKIKX0DER&me=A3CTFUQO50WGC5&merchant=A3CTFUQO50WGC5&redirect=true'
        # start_url2 = 'https://www.amazon.com/s/ref=sr_pg_1?me=A3QTILSGJZUURE&rh=i%3Amerchant-items&ie=UTF8&qid=1523088677'
        start_url2 = 'https://www.amazon.com/s?marketplaceID=ATVPDKIKX0DER&me=A3QTILSGJZUURE&merchant=A3QTILSGJZUURE&redirect=true'

        for start_url in [start_url2]:
            brand = re.search('https.*?me=(.*?)&', start_url, re.S)
            if brand.group(1) == 'A3CTFUQO50WGC5':
                brand = 'SYMA'
            elif brand.group(1) == 'A3QTILSGJZUURE':
                brand = 'Holy Stone'
            # print(brand)
            yield Request(url=start_url, callback=self.comm_parse,
                          meta={'brand': brand})

    def comm_parse(self, response):
        # 解析商品列表
        brand = response.meta['brand']

        doc = pq(response.text)
        page_next_url = doc('#pagnNextLink').attr('href')
        if page_next_url:
            page_next_url = 'https://www.amazon.com' + page_next_url
            yield Request(url=page_next_url, callback=self.comm_parse, dont_filter=True,
                          meta={'brand': brand})
            time.sleep(3)
        else:
            print('没有')

        for li in response.xpath('//li[contains(@class,"celwidget")]'):
            li_doc = pq(li.extract())
            # asin号
            asin = li_doc('li.celwidget').attr('data-asin')
            # 商品标题
            comm_title = li_doc('h2').attr('data-attribute')
            # 详情URL
            deal_url = li_doc('h2').parent().attr('href')
            if deal_url:
                deal_url = deal_url.split('ref=')[0]
            # 商品价格
            price = li_doc('span.a-offscreen').text()[1:]
            # 商品评论数
            reviews = li_doc('a.a-size-small').text()
            if reviews:
                reviews = reviews.split()[-1].replace(',','')
                if reviews.isdigit():
                    reviews = int(reviews)
                else:
                    reviews = 0
            else:
                reviews = 0
            # 评分
            score = li_doc('div.a-spacing-none span.a-icon-alt').text().split('out')[0]
            if score and len(score.split()) > 1:
                score = score.split()[1]
            else:
                score = 0

            result = {
                'asin': asin,
                'deal_url': deal_url,
                'brand': brand,
                'price': price,
                'comm_title': comm_title,
                'score': score,
                'reviews': reviews,
                # 'spider_time': time.strftime('%Y-%m-%d'),
            }

            # item = AmazonstoresItem()
            # for field in item.fields:
            #     if field in result.keys():
            #         item[field] = result.get(field)
            # yield item

            yield Request(url=deal_url, callback=self.parse_deal, dont_filter=True,
                          meta={'result': result})
            time.sleep(3)

    def parse_deal(self, response):
        # 解析商品详情页
        doc = pq(response.text)

        # 回答数
        answered = doc('#askATFLink').text()
        if answered:
            answered = answered.split()[0]
        else:
            answered = 0

        # 标签
        label = doc('#acBadge_feature_div span.ac-for-text')
        if label:
            label = label.text()
            if label:
                label = label.split('for')[1]
            else:
                label = 'null'
        else:
            label = 'null'
        # 卖家
        # sold_by = doc('#merchant-info').text().split('and')[0]

        sold_by = doc('#merchant-info').text()
        if sold_by:
            sold_by = sold_by.strip().split('.')[0]
        else:
            sold_by = 'Amazon'

        # new_number = re.search('<b>New</b>(.*?)from.*?& FREE shipping.', response.text, re.S)
        # if new_number:
        #     new_number = new_number.group(1)[2]
        # 卖家数
        seller_num = doc('#olp_feature_div').text()
        if seller_num:
            seller_num = seller_num.split('from')[0]
        else:
            seller_num = '1'

        # # #sims-fbt-form > div.sims-fbt-rows > fieldset > ul
        # bought_together = doc('#sims-fbt-form > div.sims-fbt-rows > fieldset > ul').text()
        # if bought_together:
        #     bought_together = bought_together

        # prodetails = doc('#prodDetails').text()
        # best_rank = re.search('Best Sellers Rank #(.*?)\s#', prodetails, re.S)
        # if best_rank:
        #     best_rank = best_rank.group(1).split('in')[0].strip()
        #     best_rank = best_rank.replace(',','')
        # else:
        #     best_rank = 'null'
        best_rank = doc('#prodDetails div.a-row.a-spacing-top-base > div.a-column.a-span6 > div.a-row.a-spacing-base').text()
        if best_rank:
            best_rank = re.search('Best Sellers Rank(.*?)in Toys & Games', best_rank, re.S)
            if best_rank:
                best_rank = best_rank.group(1).replace(',', '').strip()
            else:
                best_rank = 'none'
        # rank = doc('#prodDetails div.a-row.a-spacing-top-base > div.a-column.a-span6 > div.a-row.a-spacing-base').text()
        # if rank:
        #     best_rank = re.search('Best Sellers Rank(.*?)in Toys & Games', rank, re.S)
        #     if best_rank:
        #         best_rank = rank.group(1).replace(',', '')
        #     else:
        #         best_rank = 'none'

        # print(response)
        # print(response.meta['brand'])
        response.meta['result']['sold_by'] = sold_by
        response.meta['result']['seller_num'] = seller_num
        response.meta['result']['answered'] = answered
        response.meta['result']['label'] = label
        response.meta['result']['best_rank'] = best_rank
        response.meta['result']['spider_time'] = time.strftime('%Y%m%d')

        # print(response.meta['result'])

        item = AmazonstoresItem()
        for field in item.fields:
            # print(field)
            if field in response.meta['result'].keys():
                item[field] = response.meta['result'].get(field)
        yield item
