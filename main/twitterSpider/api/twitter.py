#!/Users/llb/xuni/Spider/bin python
# -*- coding: utf-8 -*-
"""
@Author: llb
@Contact: geektalk@qq.com
@WeChat: llber233
@project: twitterSpider
@File: twitterSpider.py
@Ide: PyCharm
@Time: 2021-05-30 17:21:20
@Desc: 
"""
import json

from ..utils.utils import join_url


class TwitterApi(object):
    """
    推特API接口
    """

    def __init__(self, mode='pc'):
        self.init_url(mode)

    def init_url(self, mode):
        """
        初始化url信息
        :return:
        """
        if mode.lower() == "mobile":
            self.base_url = "https://mobile.twitter.com/"
        elif mode.lower() == "pc":
            self.base_url = "https://twitter.com/"
        else:
            raise Exception(f"The mode cannot be set to {mode}, please set to 'pc' or 'mobile' (not case sensitive).")

        self.media_url = self.base_url + "{0}/media"
        self.likes_url = self.base_url + "{0}/likes"

        # api接口
        self.all = self.base_url + "i/api/2/notifications/all.json"

        # self.Following = self.base_url + "i/api/graphql/5GZ21_sdcuDYcNfgT3sgbA/Following"
        # self.Followers = self.base_url + "i/api/graphql/8-nEgbPoDML61atIQ6GLwQ/Followers"
        # self.UserMedia = self.base_url + "i/api/graphql/ep3EdGK189uKvABB-8uIlQ/UserMedia"
        # self.Likes = self.base_url + "i/api/graphql/OU4zjDOFfM9ZHq2aTjUNCA/Likes"
        # self.UserTweetsAndReplies = self.base_url + "i/api/graphql/Kq7XqqyDGn4Ly7Yh0AhK9w/UserTweetsAndReplies"

        self.Following = self.base_url + "i/api/graphql/4tkggrr_5_JVUwbP6qhCZw/Following"
        self.Followers = self.base_url + "i/api/graphql/88cNqAD-_icwFYSFhi9LCA/Followers"
        self.UserMedia = self.base_url + "i/api/graphql/-ClzyWY3kWmGS8BSPHgv8w/UserMedia"
        self.Likes = self.base_url + "i/api/graphql/Ay8caIt8NEaf_ulIvhl4uQ/Likes"
        self.UserTweets = self.base_url + 'i/api/graphql/1DL8zlYnR-WKbi0BUG2rzQ/UserTweets'
        self.UserTweetsAndReplies = self.base_url + "i/api/graphql/QK7vxE-PGFKv2NbajTrDfg/UserTweetsAndReplies"

        self.FollowersYouKnow = self.base_url + "i/api/graphql/Vitbmqp6_6fOiDatDzbOAQ/FollowersYouKnow"
        self.UserByScreenNameWithoutResults = self.base_url + "i/api/graphql/Vf8si2dfZ1zmah8ePYPjDQ/UserByScreenNameWithoutResults"
        self.home = self.base_url + "i/api/2/timeline/home.json"

    def API_UserByScreenNameWithoutResults(self, screen_name):
        """
        :param screen_name:
        :return:
        """
        url = self.UserByScreenNameWithoutResults
        params = {
            "variables": json.dumps({"screen_name": screen_name, "withHighlightedLabel": True})
        }
        return join_url(url, params)

    def API_Notifications(self):
        """通知API"""
        url = self.all
        params = {
            'cards_platform': 'Web-12',
            'count': '20',
            'ext': 'mediaStats,highlightedLabel',
            'include_blocked_by': '1',
            'include_blocking': '1',
            'include_can_dm': '1',
            'include_can_media_tag': '1',
            'include_cards': '1',
            'include_entities': True,
            'include_ext_alt_text': True,
            'include_ext_media_availability': True,
            'include_ext_media_color': True,
            'include_followed_by': '1',
            'include_mute_edge': '1',
            'include_profile_interstitial_type': '1',
            'include_quote_count': True,
            'include_reply_count': '1',
            'include_user_entities': True,
            'include_want_retweets': '1',
            'send_error_codes': True,
            'simple_quoted_tweet': True,
            'skip_status': '1',
            'tweet_mode': 'extended'
        }
        return join_url(url, params)

    def API_Following(self, rest_id, cursor=None, count=20) -> tuple:
        """
        正在关注
        :param rest_id: 用户id
        :param cursor: 筛选条件
        :param count: 数量
        :return:
        """
        url = self.Following
        params = {
            "variables": json.dumps({
                "userId": rest_id,
                "count": count,
                "cursor": cursor,
                "withHighlightedLabel": False,
                "withTweetQuoteCount": False,
                "includePromotedContent": False,
                "withTweetResult": False,
                "withReactions": True,

                # 新增两项
                "withSuperFollowsTweetFields": False,
                "withSuperFollowsUserFields": False,

                "withUserResults": False,
                "withNonLegacyCard": False,
                "withBirdwatchPivots": False
            })
        }

        return join_url(url, params)

    def API_Followers(self, rest_id, cursor=None, count=20) -> tuple:
        """
        关注者
        :param rest_id: 用户id
        :param cursor: 筛选条件
        :param count: 数量
        :return:
        """
        url = self.Followers
        params = {
            "variables": json.dumps({
                'userId': rest_id,
                'count': count,
                'cursor': cursor,
                'withHighlightedLabel': False,
                'withTweetQuoteCount': False,
                'includePromotedContent': False,
                'withTweetResult': False,
                'withReactions': False,
                'withUserResults': False,
                'withNonLegacyCard': True,
                'withBirdwatchPivots': False,
            })
        }
        return join_url(url, params)

    def API_FollowersYouKnow(self, rest_id, cursor=None, count=20) -> tuple:
        """
        可能认识的人
        :param rest_id: 用户id
        :param cursor: 筛选条件
        :param count: 数量
        :return:
        """
        url = self.FollowersYouKnow
        params = {"variables": json.dumps({
            'userId': rest_id,
            'count': count,
            'cursor': cursor,
            'withHighlightedLabel': False,
            'withTweetQuoteCount': False,
            'includePromotedContent': False,
            'withTweetResult': False,
            'withReactions': False,
            'withUserResults': False,
            'withNonLegacyCard': True,
            'withBirdwatchPivots': False,
        })}
        return join_url(url, params)

    def API_UserMedia(self, rest_id, cursor=None, count=20) -> tuple:
        """
        获取用户媒体
        :param rest_id: 用户id
        :param cursor: 筛选条件
        :param count: 数量
        :return:
        """
        url = self.UserMedia
        # params = {"variables": json.dumps({
        #     "userId": rest_id,
        #     "count": count,
        #     "cursor": cursor,
        #     "withHighlightedLabel": False,
        #     "withTweetQuoteCount": False,
        #     "includePromotedContent": False,
        #     "withTweetResult": False,
        #     "withReactions": False,
        #     "withUserResults": False,
        #
        #     "withClientEventToken": False,
        #     "withBirdwatchNotes": False,
        #     "withBirdwatchPivots": False,
        #     "withVoice": False,
        #     # "withNonLegacyCard": True,
        #
        #     # 新增两项
        #     "withSuperFollowsTweetFields": False,
        #     "withSuperFollowsUserFields": False,
        # })}
        #修改
        params = {"variables": json.dumps({
            "userId": rest_id,
            "count": count,
            "cursor": cursor,
            "withHighlightedLabel": False,
            "withTweetQuoteCount": False,
            "includePromotedContent": False,
            "withTweetResult": False,
            "withReactions": False,
            "withUserResults": False,

            "withClientEventToken": False,
            "withBirdwatchNotes": False,
            "withBirdwatchPivots": False,
            # "withVoice": False,
            # "withNonLegacyCard": True,

            # 新增两项
            "withSuperFollowsTweetFields": False,
            "withSuperFollowsUserFields": False,
            # 20220321新增
            "withDownvotePerspective":False,
            "withReactionsMetadata":False,
            "withReactionsPerspective":False,
            "withVoice":True,
            "__fs_dont_mention_me_view_api_enabled":False,
            "__fs_interactive_text_enabled":False,
            "__fs_responsive_web_uc_gql_enabled":False
        })}

        return join_url(url, params)

    def API_UserLikes(self, rest_id, cursor=None, count=20) -> tuple:
        """
        用户喜欢
        :param rest_id: 用户id
        :param cursor: 筛选条件
        :param count: 数量
        :return:
        """
        url = self.Likes
        params = {"variables": json.dumps({
            'userId': rest_id,
            'count': count,
            "cursor": cursor,
            'withHighlightedLabel': False,
            'withTweetQuoteCount': False,
            'includePromotedContent': False,
            'withTweetResult': False,
            'withReactions': False,
            'withUserResults': False,
            'withClientEventToken': False,
            'withBirdwatchNotes': False,
            'withBirdwatchPivots': False,
            'withVoice': False,
            'withNonLegacyCard': True,

            # 新增两项
            "withSuperFollowsTweetFields": False,
            "withSuperFollowsUserFields": False,
        })}
        return join_url(url, params)

    def API_UserTweets(self, rest_id, cursor=None, count=20) -> tuple:
        """
        用户推文
        :param rest_id: 用户id
        :param cursor: 筛选条件
        :param count: 数量
        :return:
        """
        url = self.UserTweets
        params = {"variables": json.dumps({
            'userId': rest_id,
            'count': count,
            'cursor': cursor,
            'withHighlightedLabel': True,
            'withTweetQuoteCount': True,
            'includePromotedContent': True,
            'withTweetResult': False,
            'withReactions': False,
            'withUserResults': False,
            'withVoice': False,
            'withNonLegacyCard': True,
            'withBirdwatchPivots': False
        })}
        return join_url(url, params)

    def API_UserTweetsAndReplies(self, rest_id, cursor=None, count=20) -> tuple:
        """
        推文和回复
        :param rest_id: 用户id
        :param cursor: 筛选条件
        :param count: 数量
        :return:
        """
        url = self.UserTweetsAndReplies
        params = {"variables": json.dumps({
            'userId': rest_id,
            'count': count,
            'cursor': cursor,
            'withHighlightedLabel': True,
            'withTweetQuoteCount': True,
            'includePromotedContent': True,
            'withTweetResult': False,
            'withReactions': False,
            'withUserResults': False,
            'withVoice': False,
            'withNonLegacyCard': True,
            'withBirdwatchPivots': False,

            # 新增两项
            "withSuperFollowsTweetFields": False,
            "withSuperFollowsUserFields": False,
        })}
        return join_url(url, params)

    def API_home(self, rest_id=None, cursor=None, count=20) -> tuple:
        """刷推特"""
        url = self.home
        params = {
            'include_profile_interstitial_type': '1',  # 包括配置文件插页式类型
            'include_blocking': '1',  # 包括阻塞
            'include_blocked_by': '1',  # 包括被阻止
            'include_followed_by': '1',  # 包括关注过的
            'include_want_retweets': '1',  # 包括想要转发
            'include_mute_edge': '1',  # 包括静音边缘
            'include_can_dm': '1',
            'include_can_media_tag': '1',  # 包括媒体标签
            'skip_status': '1',  # 跳过状态
            'cards_platform': 'Web-12',
            'include_cards': '1',
            'include_ext_alt_text': True,
            'include_quote_count': True,
            'include_reply_count': '1',
            'tweet_mode': 'extended',
            'include_entities': True,
            'include_user_entities': True,
            'include_ext_media_color': True,
            'include_ext_media_availability': True,
            'send_error_codes': True,
            'simple_quoted_tweet': True,
            'earned': '1',
            'count': count,
            'lca': True,
            'cursor': cursor,
            'ext': 'mediaStats,highlightedLabel',
        }

        return url, params
