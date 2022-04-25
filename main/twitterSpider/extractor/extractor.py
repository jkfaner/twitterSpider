import json

from .. import items
from ..extractor.json_path_finder import JsonDataFinder
from ..utils import utils


class ExtractorApi(object):
    """
    数据提取器接口
    """

    def finder(self, resp):
        if isinstance(resp, dict):
            resp = resp.get('data', resp)
        elif isinstance(resp, str):
            _resp = json.loads(resp)
            resp = _resp.get('data', resp)
        finder = JsonDataFinder(resp)
        return finder

    def find_exists(self, resp, target: str) -> bool:
        """
        检查是否存在
        :return:
        """
        finder = self.finder(resp)
        exists = finder.find_first(target)
        if exists:
            return True
        return False

    def find_all_data(self, resp, target: str):
        """
        提取target下所有数据
        :param resp:
        :param target:
        :return:
        """
        finder = self.finder(resp)
        target_list = finder.find_all_data(target)
        if not target_list:
            return None
        if not isinstance(target_list, list):
            target_list = [target_list]
        return target_list

    def find_all_last_data(self, resp, target: str):
        """
        提取target下 的父级target值 或叫做 所有单个列表中最后一个target值
        :param resp:
        :param target:
        :return:
        """
        finder = self.finder(resp)
        target_list = finder.find_all_last_data(target)
        return target_list

    def find_first_data(self, resp, target: str):
        """
        提取target下第一个数据
        :param resp:
        :param target:
        :return:
        """
        finder = self.finder(resp)
        first_target = finder.find_first_data(target)
        return first_target

    def find_last_data(self, resp, target: str):
        """
        提取target下第最后一个数据
        :param resp:
        :param target:
        :return:
        """
        finder = self.finder(resp)
        first_target = finder.find_last_data(target)
        return first_target

    def find_assign_data(self, resp, target: str, index: int):
        """
        提取target下第index个数据
        :param resp:
        :param target:
        :param index:
        :return:
        """
        finder = self.finder(resp)
        assign_target = finder.find_assign_data(target, index)
        return assign_target

    def find_all_same_level_data(self, resp, target: str):
        finder = self.finder(resp)
        target_list = finder.find_all_same_level_data(target)
        return target_list

    def find_effective_data(self, resp, target: str):
        """
        获取有效数据
        推特有效数据默认排除最后两个
        :param resp:
        :param target:
        :return:
        """
        finder = self.finder(resp)
        target_list = finder.find_all_data(target)
        return target_list[:-2]


class BaseExtractor(ExtractorApi):

    @staticmethod
    def data_to_list(data):
        if not isinstance(data, list):
            data = [data]
        return data

    @staticmethod
    def find_hashtags(data):
        """标签"""
        finder = JsonDataFinder(data)
        hashtags = finder.find_first_data('hashtags')
        if hashtags:
            finder = JsonDataFinder(hashtags)
            hashtags_text = finder.find_all_data('text')
            return hashtags_text

    @staticmethod
    def get_urls(data):
        finder = JsonDataFinder(data)
        urls = finder.find_all_data('urls')
        if urls:
            finder = JsonDataFinder(urls)
            expanded_url = finder.find_all_data('expanded_url')
            if not isinstance(expanded_url, list):
                expanded_url = [expanded_url]
            return expanded_url

    def entities(self, item):
        entities = self.find_first_data(item, 'entities')
        if not entities:
            return {}
        user_entities = items.Entities()
        user_entities['hashtags_list'] = self.find_hashtags(entities)
        user_entities['media'] = self.get_media(entities)
        user_entities['urls_list'] = self.get_urls(entities)
        return dict(user_entities)

    def extended_entities(self, data):
        extended_entities = self.find_first_data(data, 'extended_entities')
        if not extended_entities:
            return []
        # 媒体
        media = self.get_media(extended_entities)
        return media

    def get_media(self, data) -> list:
        media = self.find_first_data(data, 'media')
        if not media:
            return []
        id_strs = self.data_to_list(self.find_all_data(media, 'id_str'))
        expanded_urls = self.data_to_list(self.find_all_data(media, 'expanded_url'))
        media_urls = self.data_to_list(self.find_all_data(media, 'media_url_https'))
        types = self.data_to_list(self.find_all_data(media, 'type'))
        urls = self.data_to_list(self.find_all_data(media, 'url'))
        media_keys = self.data_to_list(self.find_all_data(media, 'media_key'))
        video_infos = self.data_to_list(self.find_all_data(media, 'video_info'))

        zip_info = zip(id_strs, types, media_urls, urls, expanded_urls, media_keys, video_infos)

        info = list()
        for id_str, media_type, media_url, url, expanded_url, media_key, video_info in zip_info:
            media = items.Media()
            media['id_str'] = id_str
            media['media_type'] = media_type
            media['media_url'] = media_url
            media['url'] = url
            media['expanded_url'] = expanded_url
            media['media_key'] = media_key
            media['video_info'] = video_info
            info.append(dict(media))
        return info


class Extractor(BaseExtractor):


    @staticmethod
    def twitter_conversion(item):
        return utils.twitter_conversion(item)

    @staticmethod
    def check_type_is_list(data):
        if isinstance(data, str) or isinstance(data, int):
            data = [str(data)]
        return data

    def user_info(self, item) -> dict:
        user_info = items.UserInfoItem()
        user_info['name'] = self.find_first_data(item, 'name')
        user_info['screen_name'] = self.find_first_data(item, 'screen_name')
        user_info['location'] = self.find_first_data(item, 'location')
        user_info['created_at'] = self.twitter_conversion(self.find_first_data(item, 'created_at'))
        user_info['friends_count'] = self.find_first_data(item, 'friends_count')
        user_info['followers_count'] = self.find_first_data(item, 'followers_count')
        user_info['favourites_count'] = self.find_first_data(item, 'favourites_count')
        user_info['media_count'] = self.find_first_data(item, 'media_count')
        user_info['description'] = self.find_first_data(item, 'description')
        user_info['profile_banner_url'] = self.find_first_data(item, 'profile_banner_url')
        user_info['profile_image_url_https'] = self.find_first_data(item, 'profile_image_url_https')
        user_info['user_entities'] = self.entities(item)
        return dict(user_info)

    def user_data(self, item) -> dict:
        media_info = items.MediaInfoItem()
        media_info['user_id_str'] = self.find_first_data(item, 'user_id_str')
        media_info['conversation_id_str'] = self.find_first_data(item, 'conversation_id_str')
        media_info['twitter_created_at'] = self.twitter_conversion(self.find_first_data(item, 'created_at'))
        media_info['full_text'] = self.find_first_data(item, 'full_text')
        media_info['favorite_count'] = self.find_first_data(item, 'favorite_count')
        media_info['reply_count'] = self.find_first_data(item, 'reply_count')
        media_info['retweet_count'] = self.find_first_data(item, 'retweet_count')
        media_info['source'] = self.find_first_data(item, 'source')
        media_info['lang'] = self.find_first_data(item, 'lang')
        media_info['twitter_entities'] = self.entities(item)
        media_info['twitter_extended_entities'] = self.extended_entities(item)
        return dict(media_info)

    def media(self, item):
        # 获取数据来源
        entries_list = self.find_effective_data(item, target='entries')
        # 筛选数据  可能出现无效数据
        tweet_list = self.find_all_data(entries_list, target='tweet')
        # 清除不完整数据
        new_tweet_list = tweet_list.copy()
        for _ in tweet_list:
            if len(_) == 1:
                new_tweet_list.remove(_)
        if new_tweet_list:
            # 可能出现脏数据 原因未知
            user_list = self.find_all_data(new_tweet_list, 'user')
            if user_list:
                # 推特信息原创者的rest_id
                user_rest_ids = self.check_type_is_list(self.find_all_data(user_list, 'rest_id'))
                # 处理脏数据
                user_rest_id = max(user_rest_ids, key=user_rest_ids.count)
                user_rest_ids = [user_rest_id for _ in range(len(new_tweet_list))]
                # 推特rest_id
                twitter_rest_ids = self.check_type_is_list(self.find_all_last_data(new_tweet_list, 'rest_id'))
                return user_rest_ids, twitter_rest_ids, new_tweet_list
