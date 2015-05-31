__author__ = 'cliviazhou'
# -*- coding: utf-8 -*-

import scrapy
from pyquery import PyQuery as pq
from zhihu_login import config
from scrapy.http import Request
from zhihu.items import UserAnswersItem


class UserSpider(scrapy.Spider):
    name = "user"

    username = "kaifulee"
    user_url = config()['zhihuinfo']['user_url'] + username

    start_urls = [user_url]
    cookies = config()['cookies']

    i = 1

    def start_requests(self):
        yield Request(self.user_url, cookies=self.cookies, callback=self.parse_user)

    def parse_user(self, response):
        with open(self.username + '.html', 'wb') as f:
            f.write(response.body)
            f.close()
        yield Request(self.user_url + "/answers", cookies=self.cookies, callback=self.parse_user_answers)

    def parse_user_answers(self, response):
        html = response.body
        with open(self.username + '_answer_' + str(self.i) + '_.html', 'wb') as f:
            print "success"
            f.write(html)
            f.close()

        self.i += 1
        pq_body = pq(html)
        page = pq_body(".border-pager span:last a").attr('href')
        page_request = Request(self.user_url + "/answers" + str(page),
                               cookies=self.cookies,
                               callback=self.parse_user_answers)

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
            #yield items
        yield page_request