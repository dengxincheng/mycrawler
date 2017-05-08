# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from scrapy.selector import Selector
from douban_move.items import DoubanMoveItem
from redis import Redis
import  datetime
from bs4 import BeautifulSoup
import re

class MovierInfoSpider(RedisSpider):
    name = "movie_info_spider"
    # allowed_domains = ["movie.douban.com/"]
    redis_key = "douban:movie_info"
    start_urls = ['http://movie.douban.com/top250']

    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(MovierInfoSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        redisdb = Redis()
        selector = Selector(response)
        item = DoubanMoveItem()
        item["ID"] =  response.url.split("/")[-2]
        item["name"] = selector.xpath("//*[@id='content']/h1/span[1]/text()").extract_first()
        item["type"] = '/'.join(selector.xpath("//*[@id='info']/span[@property='v:genre']/text()").extract())
        item['director'] = '/'.join(selector.xpath("//*[@id='info']/span[1]/span[2]/a/text()").extract())
        item['stars'] = "/".join(selector.xpath("//*[@id='info']/span[@class='actor']/span/a/text()").extract())
        item['writer'] = '/'.join(selector.xpath("//*[@id='info']/span[2]/span[2]/a/text()").extract())
        item['update_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        # item['length'] = selector.xpath("//*[@id='info']/span[@property='v:runtime']/text()").extract_first()
        item['showtime'] = '/'.join(selector.xpath("//*[@id='info']/span[@property='v:initialReleaseDate']/text()").extract())
        item['img'] = selector.xpath("//*[@id='mainpic']/a/img/@src").extract_first()

        bsobj = BeautifulSoup(selector.xpath("//*[@id='info']").extract_first(), "lxml")
        info = bsobj.find("div",{"id":"info"}).get_text()
        length = selector.xpath("//*[@id='info']/span[@property='v:runtime']/text()").extract_first()
        if length != None:
            item['length'] =  length
        else:
            item['length'] = u"40分钟"
        country = re.findall(ur'\u5730\u533a:(.*)',info)
        item['country'] = country[0] if country else ''
        language = re.findall(ur'\u8bed\u8a00:(.*)',info)
        item['language'] = language[0] if language else ''
        return item



class MovieUrlSpider(RedisSpider):

    name = "movie_url_spider"
    redis_key = "douban:tag_urls"
    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(MovieUrlSpider, self).__init__(*args, **kwargs)
    def parse(self, response):
        redisdb = Redis()
        movie_db = Redis(db=1)

        selector = Selector(response)
        movie_urls = selector.xpath("//*[@id='content']/div/div[1]/div[2]/table/tr/td/a[1]/@href").extract()
        for url in movie_urls:
            redisdb.lpush(MovierInfoSpider.redis_key,url)
            movie_db.lpush(MovierInfoSpider.redis_key,url)


class MovieTagsSpider(RedisSpider):
    name = "movie_tags_spider"
    redis_key = "douban:start_url"

    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(MovieTagsSpider, self).__init__(*args, **kwargs)
        self.url = "https://movie.douban.com/"

    def parse(self, response):
        redisdb = Redis()
        tag_url = redisdb.scard(MovieTagsSpider.redis_key)
        selector = Selector(response)
        #xpath获取标签连接
        tags_url =  selector.xpath("//*[@id='content']/div/div[1]/table[1]/tbody/tr/td/a/@href")
        for tag in tags_url:
            link = tag.extract()
            for i in range(5):
                redisdb.lpush(MovieUrlSpider.redis_key,self.url+link+"?start="+str(i*20))