__author__ = 'cliviazhou'
# -*- coding: utf-8 -*-

import os
import json
from pyquery import PyQuery as pq
from scrapy.spider import Spider
from scrapy.http import Request
from zhihu.items import UserAnswersItem, AnswerDetailItem
from utility import read_users


class UserSpider(Spider):
    name = "user"
    username = read_users()[0]
    assert isinstance(username, str)
    print username
    i = 0

    base_url = "http://www.zhihu.com/"
    simple_url = "http://zhihu.com"
    question_url = "{0}question/".format(base_url)
    people_url = "{0}people/".format(base_url)
    login_url = "{0}login".format(base_url)

    cookie = {}
    with open(os.getcwd() + "/zhihu/spiders/cookie.json") as f:
        cookie = json.load(f)
        print cookie

    def start_requests(self):
        """
        Start request from user_url
        :rtype : response
        """
        for user in read_users():
            user_url = self.base_url + "people/" + user
            print user_url
            yield Request(user_url, cookies=self.cookie, callback=self.parse)
            yield Request(user_url + "/answers", cookies=self.cookie, callback=self.parse_user_answers)

    def parse(self, response):
        with open("{0}.html".format(str(self.i)), 'wb') as f:
            f.write(response.body)
            self.i += 1
            f.close()

    def parse_user_answers(self, response):
        html = response.body
        pq_body = pq(html)
        page = pq_body(".border-pager span:last a").attr('href')
        user = pq(pq_body(".zm-profile-header-user-detail")).attr('href').split("/")[2]
        pq_answers = pq_body(".zm-item")
        print pq_answers.__class__, len(pq_answers)
        for ans in pq_answers:
            link = pq(ans)("a").attr('href')
            title = pq(ans)("a").html()
            question_id = int(link.split('/')[2])
            answer_id = int(link.split('/')[4])
            link = self.simple_url + link
            content = pq(ans)("textarea").html()
            upvote = pq(ans)(".zm-item-vote a").attr("data-votecount")

            useransitems = UserAnswersItem()
            useransitems['user'] = user
            useransitems['question_id'] = question_id
            useransitems['answer_id'] = answer_id
            useransitems['url'] = link
            useransitems['title'] = title
            print link, user
            yield useransitems

        page_request = Request(self.people_url + user + "/answers" + str(page), callback=self.parse_user_answers)
        yield page_request
