# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class AmazonstoresItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    brand = Field()
    asin = Field()
    price = Field()
    deal_url = Field()
    comm_title = Field()
    sold_by = Field()
    score = Field()
    seller_num = Field()
    reviews = Field()
    answered = Field()
    label = Field()
    best_rank = Field()
    spider_time = Field()
