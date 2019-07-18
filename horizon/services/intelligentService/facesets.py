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


class facesetsManager(object):
    '''
    人脸库管理API，可用于人脸库的创建，删除和信息更新以及人脸库列表的查询
    '''

    def __init__(self, auth):
        self.auth = auth
        self.host = "api-aiot.horizon.ai"
        self.content_type = 'application%2Fjson'
        self._faseset_feild = set([
            'name',
            'description',
            'extra'
        ])

    def build(self, name, **kwargs):
        '''
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
            if k in self._faseset_feild:
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
            if k in self._faseset_feild:
                data.update({k: v})

        headers = {
            'host': self.host,
            'conent-type': self.content_type
        }

        authorization = self.auth.get_sign(http_method=method, path=path, params=None, headers=headers)

        # url = 'http://{0}{1}?authorization={2}'.format(self.host, path, authorization)
        url = 'http://{0}{1}'.format(self.host, path)
        print(url)

        ret, info = dohttp._put(url, data=data, auth=authorization, headers=headers)

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

        # url = 'http://{0}{1}?authorization={2}'.format(self.host, path, authorization)
        url = 'http://{0}{1}'.format(self.host, path)
        print(url)

        ret, info = dohttp._delete(url, auth=authorization)

        return ret, info

    def list(self):
        '''
        返回当前api调用者的人脸库列表
        :return:
        '''
        method = 'GET'
        path = '/openapi/v1/facesets'

        headers = {
            'host': self.host
        }

        authorization = self.auth.get_sign(http_method=method, path=path, params=None, headers=headers)

        # url = 'http://{0}{1}?authorization={2}'.format(self.host, path, authorization)
        url = 'http://{0}{1}'.format(self.host, path)
        print(url)

        ret, info = dohttp._delete(url, auth=authorization)

        return ret, info