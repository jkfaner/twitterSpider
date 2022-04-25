#!/Users/llb/xuni/Spider/bin python
# -*- coding: utf-8 -*-
"""
@Author: llb
@Contact: geektalk@qq.com
@WeChat: llber233
@project: jzsc_spider
@File: aes.py
@Ide: PyCharm
@Time: 2021-05-09 16:26:29
@Desc: aes解密
"""
import base64
import json
from Crypto.Cipher import AES


class AESEncryptDecrypt:
    iv = '0123456789ABCDEF'  # iv 偏移量
    jzsc_key = 'jo8j9wGw%6HbxfFn'  # 四库一平台 秘钥

    key = '0IqEusWFpwQoJvhwviSBNx7Dq4thVUcC'  # 自定义 秘钥 256bit
    encoding = 'utf-8'

    @classmethod
    def add_16(cls, par):
        """
        这里的密钥长度必须是16、24或32，目前16位的就够用了
        :param par:
        :return:
        """
        par = par.encode(cls.encoding)
        while len(par) % 16 != 0:
            par += b'\x00'
        return par

    @classmethod
    def _pkcs7unpadding(cls, text):
        """
        处理使用PKCS7填充过的数据
        :param text: 解密后的字符串
        :return:
        """
        length = len(text)
        unpadding = ord(text[length - 1])
        return text[0:length - unpadding]

    @classmethod
    def decrypt(cls, content):
        """
        针对json响应ASE加密数据
        AES解密，模式cbc，去填充pkcs7
        :param content: 16进制编码的加密字符串
        :return: 返回解密后的字符串
        """
        key = bytes(cls.jzsc_key, encoding=cls.encoding)
        iv = bytes(cls.iv, encoding=cls.encoding)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypt_bytes = cipher.decrypt(bytes.fromhex(content))
        result = str(decrypt_bytes, encoding='utf-8')
        result = cls._pkcs7unpadding(result)
        return json.loads(result)

    @classmethod
    def encrypt_url(cls, content):
        """
        AES加密，模式cbc
        :param content:
        :return:
        """
        key = bytes(cls.key, encoding=cls.encoding)
        iv = bytes(cls.iv, encoding=cls.encoding)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        encrypt_text = cipher.encrypt(cls.add_16(content))
        result = base64.encodebytes(encrypt_text).decode().strip()
        # print(f'加密：{result}')
        return result

    @classmethod
    def decrypt_url(cls, content):
        """
        AES解密，模式cbc
        :param content:
        :return:
        """
        key = bytes(cls.key, encoding=cls.encoding)
        iv = bytes(cls.iv, encoding=cls.encoding)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypt_text = cipher.decrypt(base64.decodebytes(content.encode(cls.encoding)))
        result = decrypt_text.decode(cls.encoding).strip('\0')
        # print(f'解密：{result}')
        return result


Aes = AESEncryptDecrypt()
