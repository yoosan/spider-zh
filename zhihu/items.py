# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhihuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class UserAnswersItem(scrapy.Item):
    question_link = scrapy.Field()
    question_id = scrapy.Field()
    answer_id = scrapy.Field()
    question_title = scrapy.Field()
    answer_content = scrapy.Field()
    answer_upvote = scrapy.Field()