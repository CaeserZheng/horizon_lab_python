#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    : passengerflow.py
@Time    : 2019/7/21 14:23
@Author  : caeser zheng
@Email   : zgl3010@qq.com
"""

import json
from horizon import dohttp
from horizon import utils
import horizon.auth as au
from horizon import config
import time

_topic_name_feild = ([
    'space',    #空间级别
    'device'    #设备级别
])

class PassergentFlowAnalysis(object):
    '''
    启用客流工具api，使用客流其他api前需要先调用的此api
    '''

    def __init__(self, auth):
        self.auth = auth
        self.host = config.get_default('default_requet_host')
        self.api_version = config.get_default('default_api_version')
        self.base_url = 'http://{0}'.format(self.host)
        self.content_type = 'application%2Fjson'

    def enable_analysis(self, space_id, enable_auto_reg=True):
        '''

        :param space_id: string	是	设备空间id
        :param enable_auto_reg:boolean 否 是否使用自动建档,true:使用自动建档功能，false:不使用自动建档功能，不传默认开启自动建档
        :return:
        '''

        method = 'POST'
        path =self.api_version + '/analysis_tools/enable'

        data = {
            'space_id': space_id,
            'enable_auto_reg': enable_auto_reg
        }

        headers = {
            'host': self.host,
            'content-type': self.content_type
        }

        authorization = self.auth.get_sign(http_method=method, path=path, params=None, headers=headers)
        url = '{0}{1}'.format(self.base_url, path)
        print(url)
        ret, info = dohttp._post(url, json.dumps(data), authorization, headers=headers)

        return ret, info

    def attach_facesets_to_space(self, space_ids, faceset_ids):
        '''
        将人脸库指定要用的设备空间，这样设备空间下的ipc上来的数据就会去检索该人脸库，确定是否属于人脸库中的人员
        :param space_ids:   	string array	是	设备空间数组
        :param faceset_ids:     string array	是	人脸库ID数组
        :return:
        '''

        method = 'POST'
        path =self.api_version + '/analysis_tools/attach_space'

        data = {
            'space_ids': space_ids,
            'faceset_ids': faceset_ids

        }

        headers = {
            'host': self.host,
            'content-type': self.content_type
        }

        authorization = self.auth.get_sign(http_method=method, path=path, params=None, headers=headers)
        url = '{0}{1}'.format(self.base_url, path)
        print(url)
        ret, info = dohttp._post(url, json.dumps(data), authorization, headers=headers)

        return ret, info

    def count_search(self, device_sn, start_time, end_time, cycle=None):
        '''
        根据指定的时间和周期，查询客流量，查询粒度为设备，
        统计维度包括设备、人脸库、性别、年龄、进店、出店,统计的不同维度的进出店客流量是人次，没有去重计算
        :param device_sn:
        :param start_time:  开始时间，ISO-8601时间
        :param end_time:    结束时间，ISO-8601时间
        :param cycle:       统计周期，可选值为hour、day，不传值时只返回总数
        :return:
        '''

        method = 'GET'
        path =self.api_version + '/analysis_tools/%s/count' % device_sn

        params = {
            'start_time': start_time,
            'end_time': end_time
        }

        headers = {
            'host': self.host
        }

        authorization = self.auth.get_sign(http_method=method, path=path, params=params, headers=headers)
        url = '{0}{1}?{2}'.format(self.base_url, path, au.get_canonical_querystring(params))
        print(url)
        ret, info = dohttp._get(url, authorization)

        return ret, info

    def visitors_search(self, device_sn, start_time, end_time, current=1, per_page=20):
        '''

        :param device_sn:
        :param start_time:
        :param end_time:
        :param current:
        :param per_page:
        :return:
        '''

        method = 'GET'
        path =self.api_version + '/analysis_tools/%s/visitors' % device_sn

        # 验证current 、per_page
        if (current and per_page):
            current = current
            per_page = per_page
        elif not (current == per_page):
            raise ValueError('current and per_page must fill in at the same time or neither')

        params = {
            'start_time': start_time,
            'end_time': end_time,
            'current': current,
            'per_page': per_page
        }

        headers = {
            'host': self.host
        }

        authorization = self.auth.get_sign(http_method=method, path=path, params=params, headers=headers)
        url = '{0}{1}?{2}'.format(self.base_url, path, au.get_canonical_querystring(params))
        print(url)

        ret, info = dohttp._get(url, auth=authorization)
        # 枚举列表是否完整
        eof = False
        if ret:
            if ret["pagination"]["current"] * ret["pagination"]["per_page"] >= ret["pagination"]["total"]:
                eof = True

        return ret, info, eof

    def visitors_sub(self,topic_name,topic_id,client_id):
        '''
        指定设备空间或设备订阅，订阅后可以通过建立websocket长连接监听到店记录的推送

        :param topic_name:  string	是	订阅的topic_name，当前支持两种订阅name，space和device
        :param topic_id:    string	是	订阅的topic_id, 当订阅name是space时，表示space_id，订阅name是device时，表示device_sn
        :param client_id:   string	是	用户自定义，用户在websocket是需要传入的标识符,长度不超过24个字符，只支持大小写和数字
        :return:
        '''
        method = 'PUT'
        path =self.api_version + '/analysis_tools/visitors/sub'

        if not topic_name in _topic_name_feild:
            raise ValueError('topic_name [%s] error!!' % topic_name)

        data = {
            'topic_name':topic_name,
            'topic_id':topic_id,
            'client_id':client_id
        }

        headers = {
            'host': self.host,
            'conent-type': self.content_type
        }

        authorization = self.auth.get_sign(http_method=method, path=path, params=None, headers=headers)

        url = '{0}{1}'.format(self.base_url, path)
        print(url)

        ret, info = dohttp._put(url, data=json.dumps(data), auth=authorization, headers=headers)

        return ret, info

    def visitor_sub_cancel(self,subscription_id):
        '''
        取消到店记录订阅发起的订阅
        :param subscription_id:
        :return:
        '''
        method = 'DELETE'
        path =self.api_version + '/analysis_tools/visitors/sub/%s' % subscription_id

        headers = {
            'host': self.host
        }

        authorization = self.auth.get_sign(http_method=method, path=path, params=None, headers=headers)

        url = '{0}{1}'.format(self.base_url, path)
        print(url)

        ret, info = dohttp._delete(url, auth=authorization)

        return ret, info

    def visitor_get(self,hobot_xpush_client_id):
        '''

        :param hobot_xpush_client_id: 订阅中定义的client_id
        :return:
        '''

        pass

