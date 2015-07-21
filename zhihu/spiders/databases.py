# -*- coding: utf-8 -*-

__author__ = 'cliviazhou'

import MySQLdb
import redis
from models import UserInfo
import elasticsearch
from models import ESModel


class UserDB:
    def __init__(self):
        self.conn = MySQLdb.connect(user='root', passwd='root', db='db_spider', charset='utf8', use_unicode=True)
        self.cursor = self.conn.cursor()

    def insert(self, userinfo):
        try:
            self.cursor.execute("INSERT INTO t_user_details (userlink, nickname, "
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


class Elastic:
    SQL = "SELECT * FROM t_user_details"

    def __init__(self):
        self._es = elasticsearch.Elasticsearch()
        self._index = "user-info-v1"
        self._conn = MySQLdb.connect(user='root', passwd='root', db='db_spider', charset='utf8', use_unicode=True)
        self._cursor = self._conn.cursor()
        self._esmodel = ESModel()

    def generate_user_model(self, userinfo, esmodel):
        doc = {
            esmodel.userlink: userinfo.user_url,
            esmodel.nickname: userinfo.nickname,
            esmodel.bio: userinfo.bio,
            esmodel.career: userinfo.career,
            esmodel.education: userinfo.education,
            esmodel.weibo: userinfo.webo,
            esmodel.business: userinfo.business,
            esmodel.location: userinfo.location,
            esmodel.upvote: userinfo.upvote,
            esmodel.thanks: userinfo.thanks,
            esmodel.collection: userinfo.collection,
            esmodel.views: userinfo.views
        }
        self._es.index(index=self._index, doc_type='info_doc', id=userinfo.user_url, body=doc)

    def import_user_es(self):
        try:
            self._cursor.execute(self.SQL)
            result_list = self._cursor.fetchall()
            for res in result_list:
                userinfo = UserInfo(_userlink=res[0], _nickname=res[1], _bio=res[2], _weibo=res[3],
                                    _location=res[4], _business=res[5], _career=res[6], _education=res[7],
                                    _upvote=res[8], _thanks=res[9], _collection=res[10], _share=res[11],
                                    _followees=res[12], _followers=res[13], _views=res[14])
                self.generate_user_model(userinfo=userinfo, esmodel=self._esmodel)
                print "Import successfully"

        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])

    def del_es_data(self):
        self._es.delete(index=self._index, doc_type='info_doc')


if __name__ == "__main__":
    r = Elastic()
    r.import_user_es()
