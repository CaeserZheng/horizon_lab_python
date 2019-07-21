#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    : passengerflow.py
@Time    : 2019/7/18 14:08
@Author  : caeser zheng
@Email   : zgl3010@qq.com
"""

import json
from horizon import dohttp
import horizon.auth as au

_line_feild = set([
    'line_type',  # 画线朝向，0为进店方向：left->right=in，up->down=in；1为出店方向：left->right=out，up->down=out
    'point',  # 点的信息见
])

_line_point_feild = set([
    'top_left_x',  # int	是	点的左上横坐标
    'top_left_y',  # int	是	点的左上纵坐标
    'bottom_right_x',  # int	是	点的右下横坐标
    'bottom_right_y'  # int	是	点的右下纵坐标
])


class PassengerFlowManager(object):
    '''
    客流机配置接口，可以用于管理客流机的划线功能，可以用于统计进出店客流以及店外途径客流的等数据
    '''

    def __init__(self, auth):
        self.auth = auth
        self.host = "api-aiot.horizon.ai"
        self.content_type = 'application%2Fjson'

    def pf_line_config(self, device_sn, lines, start_time, end_time):
        '''
        用于配置画线信息，如画线朝向，点的信息
        :param device_sn:
        :param lines:[
            {   'line_type':xx
                'point':{}
            },
            {}
        ]
        :param start_time:  指统计开始的时间
        :param end_time:    指统计结束的时间
        :return:
        '''

        method = 'POST'
        path = '/openapi/v1/passengerflow/lines_config'

        data = {
            'device_sn': device_sn,
            'lines': lines,
            'start_time': start_time,
            'end_time': end_time
        }
        headers = {
            'host': self.host,
            'content-type': self.content_type
        }

        authorization = self.auth.get_sign(http_method=method, path=path, params=None, headers=headers)
        url = 'http://{0}{1}'.format(self.host, path)
        print(url)

        ret, info = dohttp._post(url, json.dumps(data), authorization, headers=headers)

        return ret, info

    def pf_line_search(self, device_sn):
        '''
        用于查看客流的画的线的相关信息
        :param device_sn:
        :return:
        '''
        method = 'GET'
        path = '/openapi/v1/passengerflow/%s' % device_sn

        headers = {
            'host': self.host
        }

        authorization = self.auth.get_sign(http_method=method, path=path, params=None, headers=headers)
        url = 'http://{0}{1}'.format(self.host, path)
        print(url)

        ret, info = dohttp._get(url, auth = authorization)

        return ret, info

    def pf_line_switch(self, device_sn,switch_status):
        '''
        用于查看客流的画的线的相关信息
        :param device_sn:
        :param switch_status: 开关状态，0为停止，1为启动
        :return:
        '''

        method = 'PUT'
        path = '/openapi/v1/passengerflow/%s/switch' % device_sn

        data = {'switch_status':switch_status}

        headers = {
            'host': self.host,
            'content-type': self.content_type
        }

        authorization = self.auth.get_sign(http_method=method, path=path, params=None, headers=headers)
        url = 'http://{0}{1}'.format(self.host, path)
        print(url)

        ret, info = dohttp._put(url, data=data, auth=authorization, headers=headers)

        return ret, info

    def pf_line_delete(self,device_sn ):
        '''
        用于删除客流画线配置信息
        :param device_sn:
        :return:
        '''

        method = 'DELETE'
        path = '/openapi/v1/passengerflow/%s' % device_sn

        headers = {
            'host': self.host
        }

        authorization = self.auth.get_sign(http_method=method, path=path, params=None, headers=headers)
        url = 'http://{0}{1}'.format(self.host, path)
        print(url)

        ret, info = dohttp._delete(url, auth=authorization)

        return ret, info


