# -*- coding: utf-8 -*-
import json

BOT_NAME = 'twitterSpider'

SPIDER_MODULES = ['twitterSpider.spiders']
NEWSPIDER_MODULE = 'twitterSpider.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

COOKIES_ENABLED = True

DOWNLOADER_MIDDLEWARES = {
    'twitterSpider.middlewares.ProxyMiddleware': 1,
    'twitterSpider.middlewares.LoginMiddleware': 1,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    'twitterSpider.middlewares.TooManyRequestsRetryMiddleware': 300,
}

CONCURRENT_REQUESTS = 1
ITEM_PIPELINES = {
    'scrapy_redis.pipelines.RedisPipeline': 1,
    'twitterSpider.pipelines.TwitterspiderPipeline': 1,
    'twitterSpider.pipelines.TwitterResourceDownloadPipeline': 2,
    'twitterSpider.pipelines.TwitterVideoFilesPipeline': 1,
}



# >>>>>>>>>>>>>>>>>>>>>>>>> scrapy_redis redis数据库<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# 指定Redis的主机名和端口
# RedisServer
REDIS_HOST = 'localhost'
REDIS_PARAMS = None
REDIS_PORT = 6379
REDIS_DB = 0

# 调度器启用Redis存储Requests队列
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# 确保所有的爬虫实例使用Redis进行重复过滤
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# 将Requests队列持久化到Redis，可支持暂停或重启爬虫
SCHEDULER_PERSIST = False
REDIS_OVER_DATA = True
# 指定redis为set类型
REDIS_START_URLS_AS_SET = True
# Requests的调度策略，默认优先级队列
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.PriorityQueue'

# >>>>>>>>>>>>>>>>>>>>>>>>>自定义参数<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# 账号 & 密码
USERNAME = '账号'
PASSWORD = '密码'

# >>>>>>>>>>>>>>>>>>>>>>>>>日志<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
from datetime import datetime
import os
# 文件及路径，log目录需要先建好
today = datetime.now()
log_path = './log'
if not os.path.exists(log_path):
    os.makedirs(log_path)
# 是否启用日志
LOG_ENABLED = True
# 日志使用的编码
LOG_ENCODING = 'utf-8'
# 日志文件(文件名)
# LOG_FILE = "log/scrapy_{}_{}_{}.log".format(today.year, today.month, today.day,today.hour)
# 日志格式
LOG_FORMAT = '%(asctime)s [%(name)s] %(levelname)s: %(message)s'
# 日志时间格式
LOG_DATEFORMAT = '%Y-%m-%d %H:%M:%S'
# 日志级别 CRITICAL, ERROR, WARNING, INFO, DEBUG
LOG_LEVEL = 'INFO'
# 如果等于True，所有的标准输出（包括错误）都会重定向到日志，例如：print('hello')
LOG_STDOUT = False
# 如果等于True，日志仅仅包含根路径，False显示日志输出组件
LOG_SHORT_NAMES = False

# >>>>>>>>>>>>>>>>>>>>>>>>> 下载 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# 设置图片下载路径
IMAGES_STORE = '/Volumes/photo/twitter'
MEDIA_ALLOW_REDIRECTS = True  # 允许304重定向
# 设置视频下载路径
FILES_STORE = IMAGES_STORE
# 下载异常等待时间
# DOWNLOAD_TIMEOUT = 60
DOWNLOAD_WARNSIZE=0
# >>>>>>>>>>>>>>>>>>>>>>>>> 其他 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
RETRY_HTTP_CODES = [429]
# >>>>>>>>>>>>>>>>>>>>>>>>> 下载列表 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
ALLOW_DOWNLOAD = dict()
download_file = os.path.join(os.getcwd(), "download.json")
if os.path.exists:
    with open(download_file, 'r') as f:
        ALLOW_DOWNLOAD = json.load(f)