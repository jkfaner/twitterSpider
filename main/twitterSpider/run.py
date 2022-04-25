#!/Users/llb/xuni/Spider/bin python
# -*- coding: utf-8 -*-
"""
@Author: llb
@Contact: geektalk@qq.com
@WeChat: llber233
@project: scrapyTwitterSpider
@File: run.py
@Ide: PyCharm
@Time: 2021-06-15 15:56:11
@Desc: 
"""

from scrapy import cmdline

name = 'twitter'
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())
