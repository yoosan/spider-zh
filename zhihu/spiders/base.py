__author__ = 'cliviazhou'

class Url:
    def __init__(self):
        pass
    BASE_URL = "http://www.zhihu.com/"
    SIMPLE_URL = "http://zhihu.com"
    QUESTION_URL = "{0}question/".format(BASE_URL)
    PEOPLE_URL = "{0}people/".format(BASE_URL)
    LOGIN_URL = "{0}login".format(BASE_URL)