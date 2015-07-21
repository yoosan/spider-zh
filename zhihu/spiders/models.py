__author__ = 'cliviazhou'

import base


class UserInfo:
    def __init__(self, _userlink, _nickname, _bio, _upvote, _thanks,
                 _followers, _followees, _views, _weibo, _location,
                 _business, _career, _education, _collection, _share):

        self.user_url = _userlink
        self.nickname = _nickname
        self.bio = _bio
        self.upvote = _upvote
        self.thanks = _thanks
        self.followers = _followers
        self.followees = _followees
        self.views = _views
        self.webo = _weibo
        self.location = _location
        self.business = _business
        self.career = _career
        self.education = _education
        self.collection = _collection
        self.share = _share

class ESModel:

    def __init__(self):
        pass
    userlink = 'userlink'
    nickname = 'nickname'
    bio = 'biography'
    upvote = 'upvote'
    thanks = 'thanks'
    followers = 'followers'
    followees = 'followees'
    views = 'views'
    weibo = 'weibo_url'
    location = 'location'
    business = 'business'
    career = 'career'
    education = 'education'
    collection = 'collection'
    share = 'share'
