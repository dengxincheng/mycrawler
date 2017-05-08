from scrapy import cmdline
from redis import Redis
from douban_move.spiders.movespider import *
# import  datetime
# Redis().lpush("douban:start_url","https://movie.douban.com/tag/")
# cmdline.execute("scrapy crawl movie_info_spider".split())
# print datetime.datetime.now()

Redis().lpush("douban:start_url","https://movie.douban.com/tag/")
cmdline.execute("scrapy crawl movie_tags_spider".split())
if "start=180" in u"https://movie.douban.com/tag/%E7%88%B1%E6%83%85?start=180&type=T":
    print "ok"