__author__ = 'cliviazhou'
# -*- coding: utf-8 -*-

import os
import json
from pyquery import PyQuery as pq
from scrapy.spider import Spider
from scrapy.http import Request
from zhihu.items import UserAnswersItem
from models import UserInfo
from databases import UserDB
from utility import trans_str_int
from utility import import_cookies_redis
from base import Url
from databases import UserRedis


class UserSpider(Spider):
    name = "user"
    BASE_URL = "http://www.zhihu.com"
    SIMPLE_URL = "http://zhihu.com"
    QUESTION_URL = "{0}question/".format(BASE_URL)
    PEOPLE_URL = "{0}people/".format(BASE_URL)
    LOGIN_URL = "{0}login".format(BASE_URL)

    info = import_cookies_redis()
    COOKIE = dict(info[0])
    HEADERS = dict(info[1])

    def start_requests(self):
        """
        Start request from user_url
        :rtype : user about response
        """
        user_list = UserRedis().export_user_list()
        for user in user_list:
            user_url = self.BASE_URL + user
            print user_url
            yield Request("{0}/about".format(user_url), cookies=self.COOKIE,
                          headers=self.HEADERS,
                          callback=self.extract_user_details)

    def parse(self, response):

        self.extract_user_details(response=response)

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
            link = self.SIMPLE_URL + link

            useransitems = UserAnswersItem()
            useransitems['user'] = user
            useransitems['question_id'] = question_id
            useransitems['answer_id'] = answer_id
            useransitems['url'] = link
            useransitems['title'] = title
            yield useransitems

        page_request = Request(self.PEOPLE_URL + user + "/answers" + str(page),
                               cookies=self.COOKIE,
                               headers=self.HEADERS,
                               callback=self.parse_user_answers)
        yield page_request

    def extract_user_details(self, response):
        """
        extract users details
        :rtype : user_url
        """
        user_link = response.xpath("//*[@class='name']/@href").extract()[0]
        user = user_link.split('/')[2]
        nickname = response.xpath("//a[@class='name']/text()").extract()
        nickname = ''.join(nickname).strip()
        bio = response.xpath("//*[@class='bio']/@title").extract()
        bio = ''.join(bio).strip()
        weibo = response.xpath("//a[@class='zm-profile-header-user-weibo']/@href").extract()
        weibo = ''.join(weibo).strip()
        location = response.xpath("//*[@class='location item']/@title").extract()
        location = ''.join(location).strip()
        business = response.xpath("//*[@class='business item']/@title").extract()
        business = ''.join(business).strip()
        career = response.xpath("//*[@class='employment item']/@title").extract()
        career = ''.join(career).strip()
        education = response.xpath("//*[@class='education item']/@title").extract()
        education = ''.join(education).strip()
        upvote = response.xpath("//*[@id='zh-pm-page-wrap']/div[1]/div[2]/div[1]/span[2]/strong/text()").extract()
        upvote = ''.join(upvote).strip()
        upvote = trans_str_int(upvote)
        thanks = response.xpath("//*[@id='zh-pm-page-wrap']/div[2]/div[2]/div[1]/div/span[3]/strong/text()").extract()
        thanks = ''.join(thanks).strip()
        thanks = trans_str_int(thanks)
        collection = response.xpath(
            "//*[@id='zh-pm-page-wrap']/div[2]/div[2]/div[1]/div/span[4]/strong/text()").extract()
        collection = ''.join(collection).strip()
        collection = trans_str_int(collection)
        share = response.xpath("//*[@id='zh-pm-page-wrap']/div[2]/div[2]/div[1]/div/span[5]/strong/text()").extract()
        share = ''.join(share).strip()
        share = trans_str_int(share)
        followees = response.xpath("/html/body/div[3]/div[2]/div[1]/a[1]/strong/text()").extract()
        followees = ''.join(followees).strip()
        followees = trans_str_int(followees)
        followers = response.xpath("/html/body/div[3]/div[2]/div[1]/a[2]/strong/text()").extract()
        followers = ''.join(followers).strip()
        followers = trans_str_int(followers)
        views = response.xpath("//*[@class='zg-gray-normal']/strong/text()").extract()
        views = ''.join(views).strip()
        views = trans_str_int(views)
        print user, nickname, bio, upvote, thanks, followers, followees, views, weibo
        print location, business, career, education, collection, share

        if followees == 0 or followees == 0 or upvote == 0:
            return

        userinfo = UserInfo(user, nickname, bio, upvote, thanks, followers,
                            followees, views, weibo, location, business,
                            career, education, collection, share)
        db = UserDB()
        db.insert(userinfo)
        user_url = Url.PEOPLE_URL + user
        request = Request("{0}/followees".format(user_url),
                          cookies=self.COOKIE,
                          headers=self.HEADERS,
                          callback=self.extract_user_followees)
        request.meta['user'] = user
        yield request

    def extract_user_followees(self, response):
        print 'Success'
        user = response.meta['user']
        redis_user = UserRedis()
        for tmp in response.xpath('//*[@id="zh-profile-follows-list"]/div/div/a/@href'):
            followee_link = ''.join(tmp.extract()).strip()
            redis_user.import_user_redis(followee_link)
        user_url = Url.PEOPLE_URL + user
        answers_request = Request("{0}/answers".format(user_url),
                                  cookies=self.COOKIE,
                                  headers=self.HEADERS,
                                  callback=self.parse_user_answers)
        yield answers_request
