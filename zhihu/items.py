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
    user = scrapy.Field()
    question_id = scrapy.Field()
    answer_id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()


class AnswerDetailItem(scrapy.Item):
    question_id = scrapy.Field()
    answer_id = scrapy.Field()
    upvote = scrapy.Field()
    date = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
