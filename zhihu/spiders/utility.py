__author__ = 'cliviazhou'
# -*- coding: utf-8 -*-

import os
import json
import redis


def config():
    """
    :rtype : dict
    """
    with open(os.getcwd() + "/config.json", 'r') as f:
        config_info = json.load(f)
        f.close()
        return config_info


def read_users():
    with open(os.getcwd() + "/zhihu/spiders/Users_List.txt") as f:
        users_list = f.readlines()
        result_list = []
        if users_list.__len__() == 0:
            print "The users_List file is empty."
            f.close()
        else:
            for user in users_list:
                if user == "":
                    continue
                else:
                    user = user.strip("\n")
                    result_list.append(user)
            f.close()
            return result_list

def trans_str_int(string):
    if len(string) == 0:
        return 0
    else:
        return int(string)

def import_cookies_redis():

    COOKIE = {
        '_xsrf': 'de9f56efa43b3e3b10b4e3be6738213c',
        '_za': 'b62235dc-2f73-47d6-90e8-2a311f1a36c3',
        'cap_id': '"MWRkOTBhZWIwNTM5NDFiOGJjNGRhOWQwNDYwYjUzZTE=|1437124856|f7cc56058aeafc0a3727493a897a91ba2c40fd07"',
        'q_c1': '3e274d341ae1424e8a6a668f959a6f86|1437124856000|1437124856000',
        'unlock_ticket': '"QUFBQWpqRW5BQUFYQUFBQVlRSlZUUVhRcUZYT2hEMTNGakVmenFPbE1FNkstVEVQUFFXS2NBPT0='
                         '|1437124861|11dfaf6ec6e8c32d24dcae1c5582efd6b4f998d3"',
        'z_c0': '"QUFBQWpqRW5BQUFYQUFBQVlRSlZUZjFWMEZYc1QzSk9jZXE5Mk90MHJLajJRQkNCa0drNkhRPT0='
                '|1437124861|b2fa2c7ff5d9e168cef6fa0a7b62e3a62bd54646"'
    }

    HEADERS = {
        "Host": "www.zhihu.com",
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/43.0.2357.134 Safari/537.36",
        "Referer": "http://www.zhihu.com/",
        "Accept-Encoding": "gzip,deflate,sdch",
        "Accept-Language": "en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4",
    }

    rds = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
    p = rds.pipeline()
    p.hset("Info", "COOKIE", COOKIE)
    p.hset("Info", "HEADERS", HEADERS)
    p.execute()
    print 'Set COOKIE AND HEADERS successfully!'
    p.hget("Info", "COOKIE")
    cok = eval(p.execute()[0])
    p.hget("Info", "HEADERS")
    hed = eval(p.execute()[0])
    print cok, hed.__class__
    return [cok, hed]

if __name__ == "__main__":
    import_cookies_redis()
