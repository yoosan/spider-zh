__author__ = 'cliviazhou'
# -*- coding: utf-8 -*-

import os
import json
from pyquery import PyQuery as pq
from scrapy.spider import Spider
from scrapy.http import Request
from zhihu.items import UserAnswersItem
from utility import read_users
from models import UserInfo
from databases import UserDB
from utility import parseStr2Int

class UserSpider(Spider):
    name = "user"
    username = read_users()[0]
    assert isinstance(username, str)
    print username

    BASE_URL = "http://www.zhihu.com/"
    SIMPLE_URL = "http://zhihu.com"
    QUESTION_URL = "{0}question/".format(BASE_URL)
    PEOPLE_URL = "{0}people/".format(BASE_URL)
    LOGIN_URL = "{0}login".format(BASE_URL)

    cookie = {}
    with open(os.getcwd() + "/zhihu/spiders/cookie.json") as f:
        cookie = json.load(f)
        print cookie

    def start_requests(self):
        """
        Start request from user_url
        :rtype : user about response
        """
        for user in read_users():
            user_url = self.BASE_URL + "people/" + user
            print user_url
            yield Request("{0}/about".format(user_url), cookies=self.cookie, callback=self.parse)

    def parse(self, response):
        """
        :type response: object
        """
        self.extract_user_details(response=response)
        # yield Request("{0}/answers".format(user_url), cookies=self.cookie, callback=self.parse_user_answers)

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
            print link, user
            yield useransitems

        page_request = Request(self.PEOPLE_URL + user + "/answers" + str(page), callback=self.parse_user_answers)
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
        business = response.xpath("//*[@class='location item']/@title").extract()
        business = ''.join(business).strip()
        career = response.xpath("//*[@class='employment item']/@title").extract()
        career = ''.join(career).strip()
        education = response.xpath("//*[@class='education item']/@title").extract()
        education = ''.join(education).strip()
        upvote = response.xpath("//*[@id='zh-pm-page-wrap']/div[1]/div[2]/div[1]/span[2]/strong/text()").extract()
        upvote = ''.join(upvote).strip()
        upvote = parseStr2Int(upvote)
        thanks = response.xpath("//*[@id='zh-pm-page-wrap']/div[2]/div[2]/div[1]/div/span[3]/strong/text()").extract()
        thanks = ''.join(thanks).strip()
        thanks = parseStr2Int(thanks)
        collection = response.xpath(
            "//*[@id='zh-pm-page-wrap']/div[2]/div[2]/div[1]/div/span[4]/strong/text()").extract()
        collection = ''.join(collection).strip()
        collection = parseStr2Int(collection)
        share = response.xpath("//*[@id='zh-pm-page-wrap']/div[2]/div[2]/div[1]/div/span[5]/strong/text()").extract()
        share = ''.join(share).strip()
        share = parseStr2Int(share)
        following = response.xpath("/html/body/div[3]/div[2]/div[1]/a[1]/strong/text()").extract()
        following = ''.join(following).strip()
        following = parseStr2Int(following)
        followed = response.xpath("/html/body/div[3]/div[2]/div[1]/a[2]/strong/text()").extract()
        followed = ''.join(followed).strip()
        followed = parseStr2Int(followed)
        views = response.xpath("//*[@class='zg-gray-normal']/strong/text()").extract()
        views = ''.join(views).strip()
        views = parseStr2Int(views)
        print user, nickname, bio, upvote, thanks, followed, following, views, weibo
        print location, business, career, education, collection, share
        user = UserInfo(user, nickname, bio, upvote, thanks, followed, following, views,
                        weibo, location, business, career, education, collection, share)
        db = UserDB()
        db.insert(user)
        # return self.PEOPLE_URL + user
