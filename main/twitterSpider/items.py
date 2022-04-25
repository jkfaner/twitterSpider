# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TwitterspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    spider_name = scrapy.Field()
    item = scrapy.Field()


class Media(scrapy.Item):
    id_str = scrapy.Field()
    media_type = scrapy.Field()
    media_url_https = scrapy.Field()
    url = scrapy.Field()
    expanded_url = scrapy.Field()
    media_key = scrapy.Field()
    video_info = scrapy.Field()


class Entities(scrapy.Item):
    hashtags_list = scrapy.Field()
    media = scrapy.Field()
    urls_list = scrapy.Field()


class UserInfoItem(scrapy.Item):
    name = scrapy.Field()
    screen_name = scrapy.Field()
    location = scrapy.Field()
    created_at = scrapy.Field()
    friends_count = scrapy.Field()
    followers_count = scrapy.Field()
    favourites_count = scrapy.Field()
    media_count = scrapy.Field()
    description = scrapy.Field()
    profile_banner_url = scrapy.Field()
    profile_image_url_https = scrapy.Field()
    user_entities = scrapy.Field()


class MediaInfoItem(UserInfoItem):
    user_id_str = scrapy.Field()
    conversation_id_str = scrapy.Field()
    twitter_created_at = scrapy.Field()
    full_text = scrapy.Field()
    favorite_count = scrapy.Field()
    reply_count = scrapy.Field()
    retweet_count = scrapy.Field()
    source = scrapy.Field()
    lang = scrapy.Field()
    twitter_entities = scrapy.Field()
    twitter_extended_entities = scrapy.Field()


class DownloadItem(scrapy.Item):
    item = scrapy.Field()
    rest_id = scrapy.Field()
    name = scrapy.Field()
    screen_name = scrapy.Field()
    video_info = scrapy.Field()
    img_info = scrapy.Field()
    spider_name = scrapy.Field()
