# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class PostItem(scrapy.Item):
    title = scrapy.Field() 		# 貼文標題
    author = scrapy.Field() 	# 貼文作者
    nickname = scrapy.Field() 	# 貼文作者
    date = scrapy.Field() 		# 貼文日期
    content = scrapy.Field() 	# 貼文內容
    ip = scrapy.Field()			# 作者IP位址
    comments = scrapy.Field() 	# 回文內容
    score = scrapy.Field() 		# 貼文分數(獲得推文+1分; 獲得噓文-1分)
    url = scrapy.Field() 		# 貼文網址
