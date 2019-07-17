#!/usr/bin/env python
#-.- coding=utf-8 -.-
'''
__author__ = 'caeser'
__mtime__ = '2019/7/16'
'''

from horizon.compat import is_py2,is_py3
import hashlib
import json
from horizon import dohttp
import horizon.auth as au


class deviceSpaceManager(object):
    '''
    设备空间管理
    '''

    def __init__(self,auth):
        self.auth = auth
        self.host = "api-aiot.horizon.ai"
        self.content_type = 'application%2Fjson'

    def list(self,current=1,per_page=20):
        '''
        获取设备空间列表
        参考：https://iotdoc.horizon.ai/busiopenapi/part1_device_space/device_space.html#part1_0
        :param current:当前页,不填时默认为1，需要和per_page同时填/不填
        :param per_page:每页数量，不填时默认值为20
        :return:
            一个dict变量，类似 {"hash": "<Hash string>", "key": "<Key string>"}
            一个ResponseInfo对象
            一个EOF信息。
        '''

        method = 'GET'
        path = '/openapi/v1/device_spaces'

        #验证current 、per_page
        if  (current and per_page):
            current = current
            per_page = per_page
        elif not (current == per_page):
            raise ValueError('current and per_page must fill in at the same time or neither')

        params = {
            'current': current,
            'per_page' : per_page
        }

        headers = {
            'host' : self.host
        }

        authorization = self.auth.get_sign(http_method=method,path=path,params=params,headers=headers)

        url = 'http://{0}{1}?current={2}&per_page={3}&authorization={4}'.format(
            self.host , path , current,per_page , authorization
        )
        url = 'http://{0}{1}?{2}'.format(
            self.host, path, au.get_canonical_querystring(params)
        )

        print(url)

        ret, info = dohttp._get(url, '',auth=authorization)

        # 枚举列表是否完整
        eof = False
        if ret :
            if ret["pagination"]["current"] * ret["pagination"]["per_page"] >= ret["pagination"]["total"]:
                eof = True

        return ret, eof, info

    def space_info(self,space_id):
        '''
        返回指定的设备空间详细信息,主要是设备空间本身的属性信息
        :param space_id: 空间id
        :return:
        '''

        method = 'GET'
        path = '/openapi/v1/device_spaces/%s' % space_id

        params = ''

        headers = {
            'host': self.host
        }

        authorization = self.auth.get_sign(http_method=method, path=path, params=params, headers=headers)

        #url = 'http://{0}{1}?authorization={2}'.format(self.host, path, authorization)

        url = 'http://{0}{1}'.format(self.host, path)
        print(url)

        ret, info = dohttp._get(url, '',authorization)

        return ret,info

    def mkspace(self,name,**kwargs):
        '''
        创建设备空间
        :param name: 设备空间名字
        :param description: 设备空间描述
        :param extra: 其他冗余扩展信息，dict 格式
        :return:
        '''
        method = 'POST'
        path ='/openapi/v1/device_spaces'

        data = {'name':name}
        for k,v in kwargs.items():
            data.update({k:v})

        print("data----")
        print(data)

        headers = {
            'host': self.host,
            'content-type':'application%2Fjson'
        }

        authorization = self.auth.get_sign(http_method=method, path=path, params=None, headers=headers)

        #url = 'http://{0}{1}?authorization={2}'.format(self.host, path, authorization)
        url = 'http://{0}{1}'.format(self.host, path)
        print(url)

        ret, info = dohttp._post(url,json.dumps(data),authorization,'',headers=headers)

        return ret, info

    def update(self,space_id,**kwargs):
        '''
        更新当前api调用者指定的设备空间相关的字段
        :param space_id:
        :param name	string	否	设备空间名字，不超80个字符
        :param description	string	否	设备空间描述
        :param extra	string	否	设备空间其他冗余信息
        :return:
        '''
        method = 'PUT'
        path = '/openapi/v1/device_spaces/%s' % space_id

        data = {}
        for k,v in kwargs.items():
            data.update({k:v})

        print("data----")
        print(data)

        headers = {
            'host': self.host,
            'content-type': self.content_type
        }

        authorization = self.auth.get_sign(http_method=method, path=path, params=None, headers=headers)

        # url = 'http://{0}{1}?authorization={2}'.format(self.host, path, authorization)
        url = 'http://{0}{1}'.format(self.host, path)
        print(url)

        ret, info = dohttp._put(url, json.dumps(data), authorization, '', headers=headers)

        return ret, info

    def delete(self,space_id):
        '''
        删除当前api调用者指定的一个设备空间，当设备空间中有挂载设备时不能删除，需要先清除设备空间中挂载的设备后方可删除
        :param space_id:
        :return:
        '''
        method = 'DELETE'
        path = '/openapi/v1/device_spaces/%s' % space_id

        headers = {
            'host': self.host
        }

        authorization = self.auth.get_sign(http_method=method, path=path, params=None, headers=headers)

        # url = 'http://{0}{1}?authorization={2}'.format(self.host, path, authorization)
        url = 'http://{0}{1}'.format(self.host, path)
        print(url)

        ret, info = dohttp._delete(url,  auth=authorization)

        return ret, info



