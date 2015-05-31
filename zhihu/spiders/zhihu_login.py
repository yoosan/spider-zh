__author__ = 'cliviazhou'
# -*- coding: utf-8 -*-

import os
import json


def config():
    with open(os.getcwd() + "/zhihu/spiders/config.json", 'r') as f:
        config = json.load(f)
        f.close()
        return config