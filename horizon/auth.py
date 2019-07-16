#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    : auth.py
@Time    : 2019/7/16 17:53
@Author  : caeser zheng
@Email   : zgl3010@qq.com
"""
import hashlib
import hmac
import string
import time
from urllib import parse

AUTHORIZATION = "authorization"
RESERVED_CHAR_SET = set(string.ascii_letters + string.digits + '.~-_')


class Auth():
    def __init__(self, access_key, secret_key):
        self.__checkKey(access_key, secret_key)
        self.ak = access_key
        self.sk = secret_key

    @staticmethod
    def __checkKey(access_key, secret_key):
        if not (access_key and secret_key):
            raise ValueError('invalid key')

    def get_normalized_char(self, i):
        char = chr(i)
        if char in RESERVED_CHAR_SET:
            return char
        else:
            return '%%%02X' % i

    def normalize_string(self, in_str, encoding_slash=True):
        NORMALIZED_CHAR_LIST = [
            self.get_normalized_char(i) for i in range(256)
        ]
        if in_str is None:
            return ''
        # 在生成规范URI时。不需要对斜杠'/'进行编码，其他情况下都需要
        if encoding_slash:
            encode_f = lambda c: NORMALIZED_CHAR_LIST[ord(c)]
        else:
            # 仅仅在生成规范URI时。不需要对斜杠'/'进行编码
            encode_f = lambda c: NORMALIZED_CHAR_LIST[ord(c)
                                                      ] if c != '/' else c
        # 按照RFC 3986进行编码
        return ''.join([encode_f(ch) for ch in in_str])

    def get_canonical_uri(self, path):
        return self.normalize_string(path, False)

    def get_canonical_querystring(self, params):
        if params is None:
            return ''
        # 除了authorization之外，所有的query string全部加入编码
        result = [
            '%s=%s' % (k, self.normalize_string(v)) for k, v in params.items()
            if k.lower != AUTHORIZATION
        ]
        # 按字典序排序
        result.sort()
        # 使用&符号连接所有字符串并返回
        return '&'.join(result)

    def get_canonical_headers(self, headers):
        headers = headers or {}

        headers_to_sign = {"host", "content-type"}

        # 对于header中的key，去掉前后的空白之后需要转化为小写
        # 对于header中的value，转化为str之后去掉前后的空白
        f = lambda k_v: (k_v[0].strip().lower(), str(k_v[1]).strip())

        result = []
        for k, v in map(f, headers.items()):
            if k in headers_to_sign:
                result.append(
                    "%s:%s" %
                    (self.normalize_string(k), self.normalize_string(v)))
        # 按照字典序排序
        result.sort()
        # 使用\n符号连接所有字符串并返回
        return '\n'.join(result)

    def __sign_key(self, timestamp):
        # 1.生成sign key
        # 1.1.生成auth-string，格式为：horizon-auth-v1/{accessKeyId}/{timestamp}
        sign_key_info = 'horizon-auth-v1/%s/%d' % (self.ak, timestamp)
        # 1.2.使用auth-string加上SK，用SHA-256生成sign key
        sign_key = hmac.new(bytes(self.sk, encoding='utf8'),
                            bytes(sign_key_info, encoding='utf8'),
                            hashlib.sha256).hexdigest()

        return sign_key_info, sign_key

    def __token(self, timestamp, data):
        # 6.使用5中生成的签名串和1中生成的sign key，用SHA-256算法生成签名结果
        sign_key_info, sign_key = self.__sign_key(timestamp)

        sign_result = hmac.new(bytes(sign_key, encoding='utf8'),
                               bytes(data, encoding='utf8'),
                               hashlib.sha256).hexdigest()

        # 7.拼接最终签名结果串
        return '%s/%s' % (sign_key_info, sign_result)

    '''
    def urlparse(self,url):
        url_list = parse.urlparse(url)
        path = '%s%s' % (url_list[1],url_list[2])

        if '#' in url:
            params = '%s#%s' % (url_list[4],url_list[5])
        else:
            params = url_list[4]
        return path,params
    '''
    def get_sign(self, http_method, path, params, headers, timestamp=None):
        headers = headers or {}
        params = params or {}

        # 1.生成签名 时间戳
        timestamp = timestamp or int(time.time())

        # 2.生成规范化uri
        canonical_uri = self.get_canonical_uri(path)

        # 3.生成规范化query string
        canonical_querystring = self.get_canonical_querystring(params)

        # 4.生成规范化header
        canonical_headers = self.get_canonical_headers(headers)

        # 5.使用'\n'将HTTP METHOD和2、3、4中的结果连接起来，成为一个大字符串
        string_to_sign = '\n'.join([
            http_method, canonical_uri, canonical_querystring,
            canonical_headers
        ])

        return self.__token(timestamp, string_to_sign)
