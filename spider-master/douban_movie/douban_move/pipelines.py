# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from model.movieInfo import MovieInfo
from scrapy.exceptions import DropItem
from mysql_setting import  DBSession
from settings import *
from urllib2 import urlopen
import  os

class MysqlPipeline(object):
    def open_spider(self,spider):
        self.session = DBSession()
        self.imagePath = IMAGE_PATH
    def process_item(self, item, spider):
        image_name = item["name"].split(" ")[0]
        movie = MovieInfo(
            rs_movie_id  = item["ID"].encode("utf-8"),
            rs_movie_name = item["name"].encode("utf-8"),
            rs_movie_type = item["type"].encode("utf-8"),
            rs_movie_director = item["director"].encode("utf-8"),
            rs_movie_writer = item["writer"].encode("utf-8"),
            rs_movie_stars = item["stars"].encode("utf-8"),
            rs_movie_showtime = item["showtime"].encode("utf-8"),
            rs_movie_length = item["length"].encode("utf-8"),
            rs_movie_img = "/images/"+item["ID"].encode("utf-8")+".jpg",
            rs_movie_country = item["country"].encode("utf-8"),
            rs_movie_language = item["language"].encode("utf-8"),
            rs_movie_updatatime = item['update_time'].encode("utf-8")
        )
        self.session.add(movie)
        self.session.commit()
        return item
    def close_spider(self,spider,item):
        self.session.close()
        # return item



class ImgDownloadPipeline(object):
    def __init__(self):
        self.imagePath = IMAGE_PATH

    def process_item(self, item, spider):
        if not os.path.exists(self.imagePath):
            os.mkdir(IMAGE_PATH)
        image_url = item["img"]
        image = open(self.imagePath+item["ID"]+".jpg","wb")

        try:
            image.write(urlopen(image_url).read())
        except Exception,e:
            image.write(e.message+"\n"+image_url)
            print e

        return item

# 爬取记录指定条数
# class CountDropPipline(object):
#     def __init__(self):
#         self.count = 100
#
#     def process_item(self, item, spider):
#         print spider
#         if self.count == 0:
#             raise DropItem("Over item found: %s" % item)
#         else:
#             self.count -= 1
#             return item