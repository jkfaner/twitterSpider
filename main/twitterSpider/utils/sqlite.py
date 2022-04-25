#!/Users/llb/xuni/Spider/bin python
# -*- coding: utf-8 -*-
"""
@Author: llb
@Contact: geektalk@qq.com
@WeChat: llber233
@project: scrapyTwitterSpider
@File: sqlite.py
@Ide: PyCharm
@Time: 2021-06-14 21:10:24
@Desc:
"""
import json
import os
import sqlite3

from ..utils.aes import Aes


class SQLit3Connection(object):

    def __init__(self):
        db_path = os.path.join(os.path.split(os.path.dirname(__file__))[0], 'twitterLogin.db')
        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()

    def insert(self, sql):
        try:
            self.cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)
            print(sql)
            self.conn.rollback()

    def select(self, sql):
        self.cur.execute(sql)
        return self.cur.fetchone()

    def save(self, account, password, cookies):
        cookies = json.dumps(cookies)
        sql = f"INSERT INTO login(account, password,cookies) values ('{account}', '{password}','{cookies}');"
        self.insert(sql)

    def update_password(self, account, password):
        sql = f"UPDATE login SET password='{password}' WHERE account = '{account}';"
        self.insert(sql)

    def update_cookies(self, account, cookies):
        sql = f"UPDATE login SET cookies='{cookies}' WHERE account = '{account}';"
        self.insert(sql)

    def doAccountPassword(self, account: str, password: str, cookies: dict = None):
        # 密码加密
        password = Aes.encrypt_url(password)

        sql = f"SELECT * FROM login WHERE account = '{account}'"
        select_result = self.select(sql)

        # 插入
        if not select_result:
            self.save(account=account, password=password, cookies=cookies)
            return

        s_account, s_password, s_cookies = select_result

        # 更新密码
        if s_password != password:
            self.update_password(password=password, account=account)

        # 更新cookies
        if s_cookies != cookies:
            self.update_cookies(account=account, cookies=cookies)

    def doCookies(self, account: str):
        sql = f"SELECT * FROM login WHERE account = '{account}'"
        select_result = self.select(sql)
        if select_result:
            s_account, s_password, s_cookies = select_result
            return json.loads(s_cookies)
