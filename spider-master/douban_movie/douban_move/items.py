# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item,Field


class DoubanMoveItem(scrapy.Item):
    ID  = Field()
    name = Field()
    type = Field()
    director = Field()
    writer = Field()
    stars = Field()
    showtime = Field()
    length = Field()
    img = Field()
    country = Field()
    language = Field()
    update_time = Field()
