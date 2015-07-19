# -*- coding: utf-8 -*-

__author__ = 'cliviazhou'

import MySQLdb
import redis
from models import UserInfo


class UserDB:
    def __init__(self):
        self.conn = MySQLdb.connect(user='root', passwd='root', db='db_spider', charset='utf8', use_unicode=True)
        self.cursor = self.conn.cursor()

    def insert(self, userinfo):
        try:
            self.cursor.execute("INSERT INTO t_user_details (user, nickname, "
                                "bio, weibo, location, business, career, education, "
                                "upvote, thanks, collected, share, followers, followees, views) "
                                "VALUES ('%s', '%s', '%s', '%s', '%s', '%s','%s', '%s',"
                                " %d, %d, %d, %d, %d, %d, %d)" % (userinfo.user_url,
                                                                  userinfo.nickname,
                                                                  userinfo.bio,
                                                                  userinfo.webo,
                                                                  userinfo.location,
                                                                  userinfo.business,
                                                                  userinfo.career,
                                                                  userinfo.education,
                                                                  userinfo.upvote,
                                                                  userinfo.thanks,
                                                                  userinfo.collection,
                                                                  userinfo.share,
                                                                  userinfo.followers,
                                                                  userinfo.followees,
                                                                  userinfo.views))
            self.conn.commit()
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])


class UserRedis:
    _key = "UserList"

    def __init__(self):
        self._redis = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)

    def import_user_redis(self, followees):
        p = self._redis.pipeline()
        p.sadd(self._key, followees)
        p.execute()

    def export_user_list(self):
        p = self._redis.pipeline()
        p.smembers(self._key)
        res = p.execute()
        if not len(res) == 0:
            return res[0]


if __name__ == "__main__":
    r = UserRedis()
    r.export_user_list()
