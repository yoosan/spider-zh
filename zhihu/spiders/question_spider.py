__author__ = 'cliviazhou'
# -*- coding: utf-8 -*-

import scrapy
import os
import json
import zhihu_login
from scrapy.http import Request


class QuestionSpider(scrapy.Spider):

    name = "zhihu"
    allowed_domains = [zhihu_login.zhihuInfo['base_url']]

    question_id = 30319131
    question_url = zhihu_login.zhihuInfo['question_base_url'] + str(question_id)

    start_urls = [question_url]

    with open(os.getcwd()+'/spiders/config.json', 'r') as f:
        config = json.load(f)
        cookies = config['cookies']


    def start_requests(self):
        yield Request(self.question_url, cookies=self.cookies, callback=self.parse_question)

    def parse_question(self, response):
        with open('result.html', 'wb') as f:
            f.write(response.body)
        print response.body.__class__