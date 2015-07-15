__author__ = 'cliviazhou'

import base


class UserInfo:
    def __init__(self, _username, _nickname, _bio, _upvote, _thanks,
                 _followed, _following, _views, _weibo, _location,
                 _business, _career, _education, _collection, _share):

        self.user_url = base.Url.BASE_URL + _username
        self.nickname = _nickname
        self.bio = _bio
        self.upvote = _upvote
        self.thanks = _thanks
        self.followed = _followed
        self.following = _following
        self.views = _views
        self.webo = _weibo
        self.location = _location
        self.business = _business
        self.career = _career
        self.education = _education
        self.collection = _collection
        self.share = _share