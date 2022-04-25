# #!/Users/llb/xuni/Spider/bin python
# # -*- coding: utf-8 -*-
# """
# @Author: llb
# @Contact: geektalk@qq.com
# @WeChat: llber233
# @project: distributedTwitterSpider
# @File: download.py
# @Ide: PyCharm
# @Time: 2021-06-29 17:38:11
# @Desc:
# """
# import json
#
# import scrapy
# from scrapy_redis.spiders import RedisSpider
#
#
# class Download(RedisSpider):
#     name = 'download'
#
#     userInfo = "userInfo"
#     userMedia = "userMedia"
#     download = "download"
#
#     def encoding(self, txt):
#         if isinstance(txt, bytes):
#             return str(txt, encoding='utf-8')
#         return txt
#
#     def iter_get_all(self, name, match=None, count=None):
#         """
#         分批获取redis所有数据
#         :param name:
#         :return:
#         """
#         for item in self.server.hscan_iter(name=name, match=match, count=count):
#             yield item
#
#     def iter_get_all_order(self, name):
#         keys = list(set([f"{self.encoding(_).split('_')[0]}_*" for _ in self.server.hkeys(name=name)]))
#         for match in keys:
#             for item in self.server.hscan_iter(name=name, match=match):
#                 yield item
#
#     def start_requests(self):
#         """获取通知信息"""
#         import time
#         url = f'https://www.twitter.com/?_={int(time.time()*1000)}'
#         yield scrapy.Request(url=url, callback=self.get_redis)
#
#     def get_redis(self,response):
#         for item in self.iter_get_all_order(self.userMedia):
#             key, item = item
#             item = json.loads(item)
#             yield item
