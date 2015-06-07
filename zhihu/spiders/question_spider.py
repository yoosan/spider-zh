__author__ = 'cliviazhou'
# -*- coding: utf-8 -*-

import scrapy
import os
import json
from scrapy.http import Request
from selenium import webdriver


class QuestionSpider(scrapy.Spider):

    def __init__(self):
        self.driver = webdriver.Safari()
    name = "question"

    question_id = 30319131

    question_url = "http://www.zhihu.com/question/" + str(question_id)

    cookie = {}

    with open(os.getcwd() + "/zhihu/spiders/cookie.json") as f:
        cookie = json.load(f)
        print cookie

    def start_requests(self):
        self.driver.get(self.question_url)
        n = self.driver.find_element_by_class_name("zu-button-more")
        yield Request(self.question_url, cookies=self.cookie, callback=self.parse_question)
        n.click()
        self.driver.close()

    def parse_question(self, response):
        with open('result.html', 'wb') as f:
            f.write(response.body)
            f.close()
        print response.body.__class__