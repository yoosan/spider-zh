# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
from items import UserAnswersItem
from MySQLdb import cursors
from twisted.enterprise import adbapi


class ZhihuPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect(user='root', passwd='', db='db_spider', charset='utf8', use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        try:
            self.cursor.execute(
                "INSERT INTO t_user_answers (user, question_id, answer_id, url, title) "
                "VALUES ('{0:s}', {1:d}, {2:d}, '{3:s}', '{4:s}')".format(
                    item['user'].encode('utf-8'), item['question_id'], item['answer_id'],
                    item['url'].encode('utf-8'), item['title'].encode('utf-8'))
            )
            self.conn.commit()
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
        return item
