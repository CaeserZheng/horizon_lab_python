#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    : device.py
@Time    : 2019/7/17 16:02
@Author  : caeser zheng
@Email   : zgl3010@qq.com
"""

import json
from horizon_lab_python.horizon import dohttp
import horizon_lab_python.horizon.auth as au
from horizon_lab_python.horizon.utils import url_encode


class deviceManager(object):
    '''
    设备空间管理
    '''

    def __init__(self,auth):
        self.auth = auth
        self.host = "api-aiot.horizon.ai"

    def list(self,current=1,per_page=20,**kwargs):
        '''
        获取设备空间列表
        参考：https://iotdoc.horizon.ai/busiopenapi/part1_device_space/device_space.html#part1_0
        :param current:当前页,不填时默认为1，需要和per_page同时填/不填
        :param per_page:每页数量，不填时默认值为20
        :param space_id:设备空间id，不传时返回默认设备空间下的设备列表
        :param attributes:用户自定义获取信息字段，如果不传则默认返回设备通用信息，
        :return:
            一个dict变量，类似 {"hash": "<Hash string>", "key": "<Key string>"}
            一个ResponseInfo对象
            一个EOF信息。
        '''

        method = 'GET'
        path = '/openapi/v1/devices'

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

        for k,v in kwargs.items():
            params.update({k:v})

        headers = {
            'host' : self.host
        }

        authorization = self.auth.get_sign(http_method=method,path=path,params=params,headers=headers)
        query = au.get_canonical_querystring(params=params)
        print(query)

        url = 'http://{0}{1}?{2}'.format(
            self.host, path, query
        )
        print(url)

        ret, info = dohttp._get(url, '',auth=authorization)
        # 枚举列表是否完整
        eof = False
        if ret :
            if ret["pagination"]["current"] * ret["pagination"]["per_page"] >= ret["pagination"]["total"]:
                eof = True

        return ret, eof, info

    def device_info(self,device_sn,**kwargs):
        '''
        返回指定的设备空间详细信息,主要是设备空间本身的属性信息
        :param device_sn: 空间id
        :param attributes: 用户自定义获取信息字段，如果不传则默认返回设备通用信息
        :return:
        '''

        method = 'GET'
        path = '/openapi/v1/devices/%s' % device_sn

        params = {}
        for k,v in kwargs.items():
            params.update({k:v})

        headers = {
            'host': self.host
        }

        authorization = self.auth.get_sign(http_method=method, path=path, params=params, headers=headers)

        #url = 'http://{0}{1}?authorization={2}'.format(self.host, path, authorization)

        if params:
            url = 'http://{0}{1}?{2}'.format(self.host, path,au.get_canonical_querystring(params))
        else:
            url = 'http://{0}{1}'.format(self.host,path)
        print(url)

        ret, info = dohttp._get(url, '',authorization)

        return ret,info
    def update_info(self,device_sn,space_id,**kwargs):
        '''
        更改设备绑定的设备空间，以及设备位置等元信息；
        当更换设备的设备空间时，该接口是异步接口，可根据返回值的request_id请求获取异步任务状态接口获取请求状态
        :param device_sn:设备编号

        kwargs:
        space_id	string	是	目标设备空间id
        name	string	否	设备名称，长度限制80字节
        position	string	否	设备所在设备空间具体位置，长度限制80字节
        description	string	否	设备描述,长度限制512字节
        extra	string	否	设备额外信息，长度限制512字节
        '''
        method = 'PUT'
        path = '/openapi/v1/device_spaces/%s/update' % device_sn

        data = {'space_id':space_id}
        for k,v in kwargs.items():
            data.update({k:v})

        print("data----")
        print(data)

        headers = {
            'host': self.host,
            'content-type': 'application/json'
        }

        authorization = self.auth.get_sign(http_method=method, path=path, params=None, headers=headers)
        # url = 'http://{0}{1}?authorization={2}'.format(self.host, path, authorization)
        url = 'http://{0}{1}'.format(self.host, path)
        print(url)

        ret, info = dohttp._put(url, json.dumps(data), authorization, headers=headers)

        return ret, info


