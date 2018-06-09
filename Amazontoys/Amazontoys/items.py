# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class AmazontoysItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    asin = Field()
    reviews = Field()
    price = Field()
    score = Field()
    rank = Field()
    sold_by = Field()
    seller_num = Field()
    rank_num = Field()
    fenlei = Field()
    deal_url = Field()
    comm_title = Field()
    spider_time = Field()
    leibie = Field()
