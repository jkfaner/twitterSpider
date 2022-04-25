#!/Users/llb/xuni/Spider/bin python
# -*- coding: utf-8 -*-
"""
@Author: llb
@Contact: geektalk@qq.com
@WeChat: llber233
@project: twitterSpider
@File: login.py
@Ide: PyCharm
@Time: 2021-06-14 20:08:51
@Desc: 
"""

import requests
from DecryptLogin import login

from ..utils import ConfigAnalysis


class TwitterLogin(ConfigAnalysis):
    is_login = False
    # 固定值
    authorization = "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"

    def __init__(self):
        super(TwitterLogin, self).__init__()
        self.session = requests.session()

    @staticmethod
    def dict_from_cookiejar(cj):
        """Returns a key/value dictionary from a CookieJar.

        :param cj: CookieJar object to extract cookies from.
        :rtype: dict
        """

        cookie_dict = {}

        for key, value in cj.items():
            cookie_dict[key] = value.replace('"', '')

        return cookie_dict

    def OAuth2Session(self, cookies):
        OAuth2Session = {
            "authorization": self.authorization,
            "x-csrf-token": cookies.get("ct0"),
            "x-twitterSpider-active-user": 'yes',
            "x-twitterSpider-auth-type": 'OAuth2Session',
            "x-twitterSpider-client-language": 'zh-cn',
            "x-twitterSpider-polling": 'true',
            'accept': 'image/webp,image/*,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,da;q=0.7',
            'host':'mobile.twitter.com',
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
        }
        return OAuth2Session

    def login_by_account(self):
        """
        账号登录
        :return:
        """
        lg = login.Login()
        infos_return, self.session, response_text = lg.twitter(username=self.username, password=self.password)

    def get_cookies(self):
        cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
        return cookies

    def login_by_cookies(self):
        # 获取cookies
        cookies = self.doCookies(account=self.username)
        return cookies

    def login(self) -> tuple:
        cookies = self.login_by_cookies()
        if not cookies:
            self.login_by_account()
            cookies = self.get_cookies()
            self.doAccountPassword(account=self.username, password=self.password, cookies=cookies)

        # OAuth2认证
        headers = self.OAuth2Session(cookies)
        return cookies, headers


t = TwitterLogin()
twitter_login = t.login()
print("开始登陆...")

