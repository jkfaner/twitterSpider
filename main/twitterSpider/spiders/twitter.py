# -*- coding: utf-8 -*-
import json
from urllib.parse import urlsplit, unquote, urlencode

import scrapy
from scrapy import Spider
from scrapy_redis.spiders import RedisSpider

from ..api.twitter import TwitterApi
from ..extractor.extractor import Extractor
import logging

logger = logging.getLogger(__name__)


class BaseSpider(Spider, Extractor):
    entrance_user_id = None
    user_id_is_true = False

    name = 'twitter'
    redis_key = "twitter:start_urls"

    def __init__(self):
        super(BaseSpider, self).__init__()
        self.api = TwitterApi()
        self.myPipeline = None

    def choose_byOnself(self, id_strs):
        """
        选择爬取的博主
        :param id_strs:
        :return:
        """
        is_true = False
        choose = None
        while not is_true:
            input_str = input("\n请输入前面的序号确认你的账户，输入其他数字跳过：")
            if input_str.isdigit():
                choose = int(input_str)
                is_true = True
            else:
                print("请输入数字！")
        items = {num: id_str for num, id_str in enumerate(id_strs)}
        return items, choose

    def show(self, response):
        resp = json.loads(response.text)
        finder = self.find_first_data(resp, 'users')
        screen_names = self.find_all_data(finder, 'screen_name')
        names = self.find_all_data(finder, 'name')
        id_strs = self.find_all_data(finder, 'id_str')
        print("在通知API中获取到了以下几个用户：")
        for num, (name, id_str, screen_name) in enumerate(zip(names, id_strs, screen_names)):
            print(f"\t{num} {name} {id_str} {screen_name}")

        items, choose = self.choose_byOnself(id_strs)
        return items, choose

    def search_user_id(self, response=None):
        item = response.text
        self.entrance_user_id = self.find_first_data(item, 'rest_id')
        if not self.entrance_user_id:
            print("screen_name无信息，请重新输入")
        else:
            self.user_id_is_true = True

    @staticmethod
    def update_url(url, cursor):
        parsed = urlsplit(url)
        _query = unquote(parsed.query.replace('+', ''))
        variables = json.loads(_query.replace("variables=", ''))
        variables["cursor"] = cursor
        params = {
            "variables": json.dumps(variables)
        }
        url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{urlencode(params)}"
        user_id = variables.get('userId')
        return url, user_id

    def get_new_url(self, function, response):
        cursor = function(response.text, 'value')
        url, user_id = self.update_url(response.url, cursor)
        return url, user_id, cursor


class TwitterSpider(BaseSpider):

    def start_requests(self):
        """获取通知信息"""
        url = self.api.API_Notifications()
        yield scrapy.Request(url=url, callback=self.choose_user)
        # yield scrapy.Request(url=url, callback=self.TestgetUser)

    def choose_user(self, response):
        """选择要爬取的入口"""
        items, choose = self.show(response)
        self.entrance_user_id = items.get(choose, None)
        if self.entrance_user_id is None:
            while not self.user_id_is_true:
                screen_name = input("\n请输入你要爬取的screen_name：")
                url = self.api.API_UserByScreenNameWithoutResults(screen_name)
                yield scrapy.Request(url=url, callback=self.search_user_id)

        print(f"爬取入口的user_id: {self.entrance_user_id}")
        url = self.api.API_Following(self.entrance_user_id, count=100)
        logger.info(f"开始爬取关注者信息:{self.entrance_user_id}")
        self.myPipeline.rest_id_list.append(self.entrance_user_id)
        self.spider_name = 'get_following'  # 设置爬虫名 方便中间件切换
        yield scrapy.Request(url=url, callback=self.get_following)

    def get_following(self, response):
        """获取正在关注的人"""
        # 提取信息
        itemContents = self.find_exists(response.text, 'itemContent')
        # 检查是否提取完毕
        if itemContents:
            yield dict(data=json.loads(response.text),type="get_following")

            url, user_id, cursor = self.get_new_url(self.find_first_data, response)
            logger.info(f"[关注] 递归爬取:{user_id} {cursor}")
            yield scrapy.Request(url=url, callback=self.get_following)

        else:
            logger.info(f"关注者信息爬取结束:{self.entrance_user_id}")
            self.myPipeline.rest_id_list.append(self.entrance_user_id)
            user_ids = self.myPipeline.rest_id_list

            # for rest_id in user_ids:
            #     logger.info(f"[用户喜欢] 开始爬取:{rest_id}")
            #     url = self.api.API_UserLikes(rest_id=rest_id, count=100)
            #     yield scrapy.Request(url=url, callback=self.get_Likes)

            for rest_id in user_ids:
                logger.info(f"[用户媒体] 开始爬取:{rest_id}")
                url = self.api.API_UserMedia(rest_id=rest_id, count=100)
                yield scrapy.Request(url=url, callback=self.get_userMedia)

    def TestgetUser(self,response):
        rest_id = 1166057664519888896
        url = self.api.API_UserMedia(rest_id=rest_id, count=20)
        yield scrapy.Request(url=url, callback=self.get_userMedia)

    def get_userMedia(self, response):
        """获取媒体信息"""
        # tweet = self.find_exists(response.text, 'tweet')
        tweet = self.find_exists(response.text, 'itemContent')
        # 检查是否提取完毕
        if tweet:
            yield dict(data=json.loads(response.text),type="get_userMedia")

            url, user_id, cursor = self.get_new_url(self.find_last_data, response)
            logger.info(f"[媒体] 递归爬取:{user_id} {cursor}")
            yield scrapy.Request(url=url, callback=self.get_userMedia)

    def get_Likes(self, response):
        tweet = self.find_exists(response.text, 'tweet')
        # 检查是否提取完毕
        if tweet:
            yield dict(data=json.loads(response.text),type="get_Likes")

            url, user_id, cursor = self.get_new_url(self.find_last_data, response)
            logger.info(f"[喜欢] 递归爬取:{user_id} {cursor}")
            yield scrapy.Request(url=url, callback=self.get_Likes)
