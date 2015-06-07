__author__ = 'cliviazhou'
# -*- coding: utf-8 -*-

import os
import json
from scrapy.http import Response

def config():
    with open(os.getcwd() + "/zhihu/spiders/config.json", 'r') as f:
        config_info = json.load(f)
        f.close()
        return config_info


def read_users():
    with open(os.getcwd() + "/zhihu/spiders/Users_List.txt") as f:
        users_list = f.readlines()
        if users_list.__len__() == 0:
            print "The users_List file is empty."
            f.close()
        else:
            f.close()
            return users_list
