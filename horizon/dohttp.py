#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    : dohttp.py
@Time    : 2019/7/17 10:15
@Author  : caeser zheng
@Email   : zgl3010@qq.com
"""

import platform
import requests

from horizon.compat import is_py2, is_py3
from horizon import config
from horizon.auth import RequestsAuth
from . import __version__

_sys_info = '{0}; {1}'.format(platform.system(), platform.machine())
_python_ver = platform.python_version()

USER_AGENT = 'MyHorizonApiPythonTest/{0} ({1}; ) Python/{2}'.format(
    __version__, _sys_info, _python_ver)

_session = None
_headers = {'User-Agent': USER_AGENT}

def __return_wrapper(resp):
    if resp.status_code != 200:
        return None, ResponseInfo(resp)
    resp.encoding = 'utf-8'
    ret = resp.json(encoding='utf-8') if resp.text != '' else {}
    if ret is None:  # json null
        ret = {}
    return ret, ResponseInfo(resp)

def _init():
    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(
        pool_connections=config.get_default('connection_pool'),
        pool_maxsize=config.get_default('connection_pool'),
        max_retries=config.get_default('connection_retries'))
    session.mount('http://', adapter)
    global _session
    _session = session

def _post(url, data, auth, files=None, headers=None):
    if _session is None:
        _init()
    try:
        post_headers = _headers.copy()
        if headers is not None:
            for k, v in headers.items():
                post_headers.update({k: v})
        r = _session.post(
            url,
            data=data,
            auth=RequestsAuth(auth),
            # files = files,
            headers=post_headers,
            timeout=config.get_default('connection_timeout')
        )
    except Exception as e:
        return None, ResponseInfo(None, e)
    return __return_wrapper(r)


def _put(url, data, auth, files=None, headers=None):
    if _session is None:
        _init()
    try:
        post_headers = _headers.copy()
        if headers is not None:
            for k, v in headers.items():
                post_headers.update({k: v})
        r = _session.put(
            url,
            data=data,
            # files=files,
            auth=RequestsAuth(auth),
            headers=post_headers,
            timeout=config.get_default('connection_timeout'))
    except Exception as e:
        return None, ResponseInfo(None, e)
    return __return_wrapper(r)


def _get(url, params=None, auth=None):
    try:
        r = requests.get(
            url,
            params=params,
            auth=RequestsAuth(auth) if auth is not None else None,
            timeout=config.get_default('connection_timeout'),
            headers=_headers)
    except Exception as e:
        return None, ResponseInfo(None, e)
    if r.json()['code'] != 0:
        return None, ResponseInfo(r)
    return __return_wrapper(r)


def _delete(url, data=None ,params=None, auth=None):
    try:
        r = requests.delete(
            url,
            data=data,
            params=params,
            auth=RequestsAuth(auth) if auth is not None else None,
            timeout=config.get_default('connection_timeout'),
            headers=_headers
        )
    except Exception as e:
        return None, ResponseInfo(None, e)
    return __return_wrapper(r)


class ResponseInfo(object):
    """七牛HTTP请求返回信息类
    该类主要是用于获取和解析对七牛发起各种请求后的响应包的header和body。
    Attributes:
        status_code: 整数变量，响应状态码
        text_body:   字符串变量，响应的body
        error:       字符串变量，响应的错误内容
    """

    def __init__(self, response, exception=None):
        """用响应包和异常信息初始化ResponseInfo类"""
        self.__response = response
        self.exception = exception
        if response is None:
            self.status_code = -1
            self.text_body = None
            self.error = str(exception)
        else:
            ''''
            self.status_code = response.status_code
            self.text_body = response.text
            
            if self.status_code >= 400:
                ret = {}
                try:
                    ret = response.json() if response.text != '' else None
                except  ValueError:  # r.json() raises an exception. raises ValueError: No JSON object could be decoded
                    ret['message'] = self.text_body
                    ret['code'] = self.status_code
                if ret is None or ret['message'] is None:
                    self.error = 'unknown'
                else:
                    self.error = '{"code":%d","message":%s}' % (ret['code'] , ret['message'])
        
        '''
            self.status_code = response.status_code
            self.text_body = response.text
            ret = {}
            try:
                ret = response.json() if response.text!='' else None
                if ret['code'] != 0:
                    self.status_code = -1
                    self.text_body = response
                    self.error ='{"code":%d,"message":%s,"request_id":%s}' % \
                                 (ret['code'],ret['message'],ret['request_id'])
                else:
                    self.status_code = response.status_code
                    self.text_body = response.text
            except  ValueError:  # r.json() raises an exception. raises ValueError: No JSON object could be decoded
                ret['message'] = self.text_body
                ret['code'] = self.status_code
            if ret is None or ret['message'] is None:
                self.error = 'unknown'
            else:
                self.error = '{"code":%d","message":%s}' % (ret['code'] , ret['message'])

    def ok(self):
        return self.status_code == 200

    def need_retry(self):
        if self.__response is None or self.req_id is None:
            return True
        code = self.status_code
        if (code // 100 == 5 and code != 579) or code == 996:
            return True
        return False

    def connect_failed(self):
        return self.__response is None or self.req_id is None

    def __str__(self):
        if is_py2:
            return ', '.join(
                ['%s:%s' % item for item in self.__dict__.items()]).encode('utf-8')
        elif is_py3:
            return ', '.join(['%s:%s' %
                              item for item in self.__dict__.items()])

    def __repr__(self):
        return self.__str__()
