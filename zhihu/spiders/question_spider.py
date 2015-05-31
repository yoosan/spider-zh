__author__ = 'cliviazhou'
# -*- coding: utf-8 -*-

import scrapy
import os
import json
import zhihu_login
from scrapy.http import Request
from zhihu_login import config


class QuestionSpider(scrapy.Spider):

    name = "question"
    allowed_domains = [config()['zhihuinfo']['base_url']]

    question_id = 30319131
    question_url = config()['zhihuinfo']['question_base_url'] + str(question_id)

    start_urls = [question_url]
    cookies = config()['cookies']

    def start_requests(self):
        yield Request(self.question_url, cookies=self.cookies, callback=self.parse_question)

    def parse_question(self, response):
        with open('result.html', 'wb') as f:
            f.write(response.body)
            f.close()
        print response.body.__class__