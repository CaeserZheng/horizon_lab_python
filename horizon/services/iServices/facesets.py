#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    : facesets.py
@Time    : 2019/7/18 14:20
@Author  : caeser zheng
@Email   : zgl3010@qq.com
"""

import json
from horizon import dohttp
import horizon.auth as au

_faseset_feild = set([
    'name',
    'description',
    'extra'
])


class FaceSetsManager(object):
    '''
    人脸库管理API，可用于人脸库的创建，删除和信息更新以及人脸库列表的查询
    '''

    def __init__(self, auth):
        self.auth = auth
        self.host = "api-aiot.horizon.ai"
        self.content_type = 'application%2Fjson'

    def build(self, name, **kwargs):
        '''
        为当前api调用者创建人脸库
        :param
        name	string	是	人脸库名, 长度限制80字符
        extra	string	否	人脸库额外信息，长度限制512字符
        description	string	否	人脸库描述，长度限制512字符
        :return:
        '''

        method = 'POST'
        path = '/openapi/v1/facesets'

        data = {'name': name}
        for k, v in kwargs.items():
            if k in _faseset_feild:
                data.update({k: v})

        headers = {
            'host': self.host,
            'content-type': self.content_type
        }

        authorization = self.auth.get_sign(http_method=method, path=path, params=None, headers=headers)
        # url = 'http://{0}{1}?authorization={2}'.format(self.host, path, authorization)
        url = 'http://{0}{1}'.format(self.host, path)
        print(url)
        ret, info = dohttp._post(url, json.dumps(data), authorization, headers=headers)

        return ret, info

    def delete(self, faceset_id):
        '''
        删除当前api调用者指定的人脸库
        :param faceset_id:
        :return:
        '''
        method = 'DELETE'
        path = '/openapi/v1/facesets/%s' % faceset_id

        headers = {
            'host': self.host
        }

        authorization = self.auth.get_sign(http_method=method, path=path, params=None, headers=headers)

        # url = 'http://{0}{1}?authorization={2}'.format(self.host, path, authorization)
        url = 'http://{0}{1}'.format(self.host, path)
        print(url)

        ret, info = dohttp._delete(url, auth=authorization)

        return ret, info

    def update(self, faceset_id, **kwargs):
        '''
        更新当前api调用者指定的人脸库相关的字段
        :param faceset_id:

        name	string	否	更改后的人脸库名，长度限制80字符
        extra	string	否	更改后的人脸库额外信息，长度限制512字符
        description	string	否	人脸库描述，长度限制512字符
        :return:
        '''
        method = 'PUT'
        path = '/openapi/v1/facesets/%s' % faceset_id

        data = {}
        for k, v in kwargs.items():
            if k in _faseset_feild:
                data.update({k: v})

        headers = {
            'host': self.host,
            'conent-type': self.content_type
        }

        authorization = self.auth.get_sign(http_method=method, path=path, params=None, headers=headers)

        url = 'http://{0}{1}'.format(self.host, path)
        print(url)

        ret, info = dohttp._put(url, data=json.dumps(data), auth=authorization, headers=headers)

        return ret, info

    def search(self, faceset_id):
        '''

        :param faceset_id:
        :return:
        '''
        method = 'GET'
        path = '/openapi/v1/facesets/%s' % faceset_id

        headers = {
            'host': self.host
        }

        authorization = self.auth.get_sign(http_method=method, path=path, params=None, headers=headers)
        url = 'http://{0}{1}'.format(self.host, path)
        print(url)

        ret, info = dohttp._get(url, auth=authorization)

        return ret, info

    def list(self, current=1, per_page=20):
        '''
        获取设备空间列表
        参考：https://iotdoc.horizon.ai/busiopenapi/part1_device_space/device_space.html#part1_0
        :param current:当前页,不填时默认为1，需要和per_page同时填/不填
        :param per_page:每页数量，不填时默认值为20
        :param space_id:设备空间id，不传时返回默认设备空间下的设备列表
        attributes={name,capture_config}
            name          模块
            capture_config 配置
        :return:
            一个dict变量，类似 {"hash": "<Hash string>", "key": "<Key string>"}
            一个ResponseInfo对象
            一个EOF信息。
        '''

        method = 'GET'
        path = '/openapi/v1/facesets'

        # 验证current 、per_page
        if (current and per_page):
            current = current
            per_page = per_page
        elif not (current == per_page):
            raise ValueError('current and per_page must fill in at the same time or neither')

        params = {
            'current': current,
            'per_page': per_page,
        }

        headers = {
            'host': self.host
        }

        authorization = self.auth.get_sign(http_method=method, path=path, params=params, headers=headers)
        query = au.get_canonical_querystring(params=params)

        url = 'http://{0}{1}?{2}'.format(
            self.host, path, query
        )
        print(url)

        ret, info = dohttp._get(url, auth=authorization)
        # 枚举列表是否完整
        eof = False
        if ret:
            if ret["pagination"]["current"] * ret["pagination"]["per_page"] >= ret["pagination"]["total"]:
                eof = True

        return ret, info, eof
