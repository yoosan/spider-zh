__author__ = 'cliviazhou'
# -*- coding: utf-8 -*-

import os
import json


def config():
    """

    :rtype : dict
    """
    with open(os.getcwd() + "/cookie.json", 'r') as f:
        config_info = json.load(f)
        print config_info
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


if __name__ == "__main__":
    config()
