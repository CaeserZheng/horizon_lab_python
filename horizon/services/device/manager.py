#!/usr/bin/env python
#-.- coding=utf-8 -.-
'''
__author__ = 'caeser'
__mtime__ = '2019/7/16'
'''

from horizon.compat import is_py2,is_py3
import hashlib
import json

def urlencode(str):
    if is_py2:
        import urllib2
        return urllib2.quote(str)
    elif is_py3:
        import urllib.parse
        return urllib.parse.quote(str)



class deviceSpaceManager(object):
    '''
    设备空间管理
    '''

    def __init__(self,auth):
        self.auth = auth
        self.host = "api-aiot.horizon.ai"

    def list(self,current=None,per_page=None):
        '''
        获取设备空间列表
        :param current:当前页,不填时默认为1，需要和per_page同时填/不填
        :param per_page:每页数量，不填时默认值为20
        :return:
        '''

        method = 'GET'
        path = '/openapi/v1/device_spaces'

        current = 1         #current 默认为1
        per_page = 20       #per_page 默认为2

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

        print(url)


