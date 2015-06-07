__author__ = 'cliviazhou'
# -*- coding: utf-8 -*-

import os
import json
from pyquery import PyQuery as pq
from scrapy.spider import Spider
from scrapy.http import Request
from zhihu.items import UserAnswersItem
from utility import read_users


class UserSpider(Spider):

    name = "user"
    username = read_users()[0]

    base_url = "http://www.zhihu.com/"
    login_url = base_url + "login"

    user_url = base_url + "people/" + username

    start_urls = [user_url]
    cookie = {}

    with open(os.getcwd() + "/zhihu/spiders/cookie.json") as f:
        cookie = json.load(f)
        print cookie

    def start_requests(self):
        yield Request(self.user_url, cookies=self.cookie, callback=self.parse_user)

    def parse_user(self, response):
        with open(self.username + '.html', 'wb') as f:
            f.write(response.body)
            f.close()
        yield Request(self.user_url + "/answers", cookies=self.cookie, callback=self.parse_user_answers)

    def parse_user_answers(self, response):
        html = response.body
        pq_body = pq(html)
        page = pq_body(".border-pager span:last a").attr('href')
        with open(self.username + '_answer_' + str(page) + '_.html', 'wb') as f:
            print "success"
            f.write(html)
            f.close()
        page_request = Request(self.user_url + "/answers" + str(page), callback=self.parse_user_answers)

        pq_answers = pq_body(".zm-item")
        print pq_answers.__class__, len(pq_answers)
        for ans in pq_answers:
            link = pq(ans)("a").attr('href')
            title = pq(ans)("a").html()
            content = pq(ans)("textarea").html()
            upvote = pq(ans)(".zm-item-vote a").attr("data-votecount")

            items = UserAnswersItem()
            items['question_link'] = link
            items['question_title'] = title
            items['answer_content'] = content
            items['answer_upvote'] = upvote
            print link, upvote
        yield page_request