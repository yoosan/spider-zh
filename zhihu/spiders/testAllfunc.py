# coding=utf-8
from utility import read_users
import MySQLdb
# -*- coding: utf-8 -*-


def testRead():
    print read_users()
    for usr in read_users():
        print usr


def loadDb():
    conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='', db='db_spider', port=3306, charset="utf8")
    cur = conn.cursor()
    a = "再试一次"
    print len(a)
    #a = a.decode("gbk", "ignore").encode("utf-8")
    #print a
    cur.execute("insert into t_answers_detail(question_id,url) values (111, '%s')" % a)
    #print cur.fetchall()
    #cur.close()
    conn.commit()
    conn.close()