# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import os
from urllib.parse import quote

import scrapy
from scrapy.pipelines.files import FilesPipeline
from scrapy.pipelines.images import ImagesPipeline
from scrapy_redis.pipelines import RedisPipeline

from . import items
from .extractor.extractor import Extractor
from .settings import REDIS_OVER_DATA, ALLOW_DOWNLOAD

logger = logging.getLogger(__name__)


class TwitterspiderPipeline(RedisPipeline, Extractor):
    userInfo = "userInfo"
    userMedia = "userMedia"
    download = "download"

    def __init__(self, server):
        super(TwitterspiderPipeline, self).__init__(server)
        self.rest_id_list = list()

    def open_spider(self, spider):
        spider.myPipeline = self

    def save_process_item(self, name, key, value):
        if REDIS_OVER_DATA:
            self.server.hset(name=name, key=key, value=self.serialize(value))
        else:
            if not self.server.hexists(name=name, key=key):
                self.server.hset(name=name, key=key, value=self.serialize(value))

    def _process_item(self, item, spider):
        spider_name = item["type"]
        if spider.name == "twitter":
            if spider_name == 'get_following':
                # 提取用户信息
                self.extractor_rest_id(item)
                self.extractor_user(item, spider)
        # elif spider_name == 'get_userMedia' or spider_name == 'get_Likes':
        #     self.extractor_media(item, spider)
        return item

    def extractor_rest_id(self, item):
        """提取rest_id"""
        itemContents = self.find_all_data(item, 'itemContent')
        # 下载所有关注
        # self.rest_id_list.extend([self.find_first_data(itemContent, 'rest_id') for itemContent in itemContents])
        # 下载download.json中的数据（名字为推特昵称）
        for itemContent in itemContents:
            if self.find_first_data(itemContent, "name") in ALLOW_DOWNLOAD['name_lists']:
                self.rest_id_list.append(self.find_first_data(itemContent, 'rest_id'))

        logger.info(f"[{len(itemContents)}/{len(self.rest_id_list)}]关注者数据")

    def extractor_user(self, item, spider):
        """提取用户个人信息"""
        itemContents = self.find_all_data(item, 'itemContent')
        logger.info(f"提取个人信息...共:{len(itemContents)}条")
        for itemContent in itemContents:
            if not isinstance(itemContent, dict):
                continue
            only_key = self.find_first_data(itemContent, 'rest_id')
            info = {only_key: self.user_info(itemContent)}
            effective = any([True if item else False for key, item in info[only_key].items()])
            if effective:
                self.save_process_item(name=self.userInfo, key=only_key, value=info)

    def extractor_media(self, item, spider):
        logger.info(f"提取推特信息...")
        date = self.media(item)
        for user_rest_id, twitter_rest_id, tweet in zip(date):
            # 保存数据
            only_key = f'{user_rest_id}_{twitter_rest_id}'
            self.save_process_item(name=self.userMedia, key=only_key, value=tweet)


class BaseDownload(Extractor):

    def get_download_data(self, tweet):
        download = items.DownloadItem()
        download['rest_id'] = self.find_first_data(tweet, 'rest_id')
        download['name'] = self.find_first_data(tweet, 'name')
        download['screen_name'] = self.find_first_data(tweet, 'screen_name')

        # 视频
        video_info = self.find_all_data(tweet, 'video_info')
        if video_info and any(video_info):
            _video_info = [_ for video in video_info if video for _ in
                           self.find_all_data(video, 'variants')]
            new_video_info = [video for video in _video_info if video.get('content_type') == "video/mp4"]
            new_video_info = sorted(new_video_info, key=lambda e: e.__getitem__('bitrate'), reverse=True)

            download['video_info'] = [new_video_info[0].get('url')]  # 取质量最好的mp4
        else:
            download['video_info'] = []

        # 图片
        url_list = self.find_all_data(tweet, 'media_url_https')
        img_list = [url for url in url_list if
                    url.lower().endswith('.jpg') or
                    url.lower().endswith('.gif') or
                    url.lower().endswith('.png') or
                    url.lower().endswith('.jpeg') or
                    url.lower().endswith('.jpeg')] if url_list else []
        download["img_info"] = list(set(img_list))
        return download

    def get_userMedia_requests(self, item):
        if item['type'] == "get_userMedia" or item['type'] == "get_Likes":
            date = self.media(item)
            for user_rest_id, twitter_rest_id, tweet in zip(*date):
                yield self.get_download_data(tweet)

    def get_filepath(self, request, path):
        """
        获取文件路径
        :param request:
        :param path:
        :return:
        """
        name = request.item.get('name')
        screen_name = request.item.get('screen_name')
        image_name = path.replace("full", "")
        category = f"{screen_name}&&{name}{image_name}"
        return category

    def show(self, medias, is_photo=True):
        for file in medias:
            if is_photo:
                logger.info(f"图片下载成功：file://{quote(file)}")
            else:
                logger.info(f"视频下载成功：file://{quote(file)}")


class TwitterResourceDownloadPipeline(ImagesPipeline):

    def __init__(self, store_uri, download_func=None, settings=None):
        super(TwitterResourceDownloadPipeline, self).__init__(store_uri, download_func, settings)
        self.base = BaseDownload()

    def get_media_requests(self, item, info):
        """
        注意:
        如果你不想使用url的hash值作为文件名，而是想使用item中的key对应的value作为文件名
        需要使用meta将部分参数添加到request中
        例如我们item中有video_name字段，我想在自定义视频名时用该字段最为文件名可以这样做
        return [Request(x, meta={'video_name': item.get('video_name', None))}) for x in item.get(self.files_urls_field, [])]
        """
        request_objs = list()
        for download in self.base.get_userMedia_requests(item):
            if download['img_info']:
                img_request_objs = [scrapy.Request(image_url) for image_url in download['img_info']]
                for request_obj in img_request_objs:
                    # 将download绑定到Request对象
                    request_obj.item = download
                request_objs.extend(img_request_objs)
        return request_objs

    def file_path(self, request, response=None, info=None):
        # 这个方式是在图片将要被存储时候调用，来获取这个图片的存储路径
        # 获取父类返回的保存地址
        path = super(TwitterResourceDownloadPipeline, self).file_path(request, response, info)
        return self.base.get_filepath(request, path)

    def item_completed(self, results, item, info):
        image_paths = [os.path.join(self.store.basedir, x['path']) for ok, x in results if ok]
        if not image_paths:
            return item
        # item['image_paths'] = image_paths
        self.base.show(image_paths)
        return item


class TwitterVideoFilesPipeline(FilesPipeline):
    def __init__(self, store_uri, download_func=None, settings=None):
        super(TwitterVideoFilesPipeline, self).__init__(store_uri, download_func, settings)
        self.base = BaseDownload()

    def get_media_requests(self, item, info):
        """
        注意:
        如果你不想使用url的hash值作为文件名，而是想使用item中的key对应的value作为文件名
        需要使用meta将部分参数添加到request中
        例如我们item中有video_name字段，我想在自定义视频名时用该字段最为文件名可以这样做
        return [Request(x, meta={'video_name': item.get('video_name', None))}) for x in item.get(self.files_urls_field, [])]
        """
        request_objs = list()
        for download in self.base.get_userMedia_requests(item):
            if download['video_info']:
                video_request_objs = list(set([scrapy.Request(image_url) for image_url in download['video_info']]))
                for request_obj in video_request_objs:
                    # 将download绑定到Request对象
                    request_obj.item = download
                request_objs.extend(video_request_objs)
        return request_objs

    def file_path(self, request, response=None, info=None):
        path = super(TwitterVideoFilesPipeline, self).file_path(request, response, info)
        return self.base.get_filepath(request, path) + '.mp4'

    def item_completed(self, results, item, info):
        image_paths = [os.path.join(self.store.basedir, x['path']) for ok, x in results if ok]
        if not image_paths:
            return item
        item['video_paths'] = image_paths
        self.base.show(image_paths, is_photo=False)
        return item
