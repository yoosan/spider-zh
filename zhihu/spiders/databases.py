# -*- coding: utf-8 -*-

__author__ = 'cliviazhou'

import MySQLdb
from models import UserInfo

class UserDB:
    def __init__(self):
        self.conn = MySQLdb.connect(user='root', passwd='root', db='db_spider', charset='utf8', use_unicode=True)
        self.cursor = self.conn.cursor()

    def insert(self, userinfo):
        try:
            self.cursor.execute("INSERT INTO t_user_details (user, nickname, "
                                "bio, weibo, location, business, career, education, "
                                "upvote, thanks, collect, share, followed, following, views) "
                                "VALUES ('%s', '%s', '%s', '%s', '%s', '%s','%s', '%s',"
                                " %d, %d, %d, %d, %d, %d, %d)" % (userinfo.user_url, userinfo.nickname,
                                                                  userinfo.bio, userinfo.webo, userinfo.location,
                                                                  userinfo.business, userinfo.career, userinfo.education,
                                                                  userinfo.upvote, userinfo.thanks, userinfo.collection,
                                                                  userinfo.share, userinfo.followed, userinfo.following,
                                                                  userinfo.views))
            self.conn.commit()
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])