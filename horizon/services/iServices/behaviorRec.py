#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    : device_behavior.py
@Time    : 2019/7/27 14:37
@Author  : caeser zheng
@Email   : zgl3010@qq.com
"""
from horizon import dohttp
from horizon import config
import json

_drive_behavior_body_feild = set([
    'request_id',  # string	否	唯一请求标识，响应中会把该值返回，用于映射会话，未提供时，系统会自动生成
    'device_id',  # string	否	终端设备ID，在有该ID的时候，可以上传该ID，系统会自动按照设备维度进行算法能力加强
    'video_type',  # int	是	0: 通过url识别，参数video_url不为空；1: 通过视频video_base64识别，参数video_base64不为空
    'video_url',  # string	否	输入视频URL
    'video_base64',
    # string	否	视频数据，视频时长不超过10s；base64编码，要求base64编码后大小不超过15M。视频的base64编码是不包含前缀头的，如(data:vedio/mp4;base64,)，支持视频格式：主流的avi/mpeg视频格式
    'detect_type'  # string	否	识别的属性行为类别，英文逗号分隔，默认所有属性都识别；smoke //吸烟，cellphone //打手机 ，close_eye//闭眼，yawn//打哈欠
])

_drive_behavior_detect_type_feild = set([
    'smoke',  # 吸烟
    'cellphone',  # 打电话
    'close_eye',  # 闭眼，
    'yawn',  # //打哈欠
])


class DriveBehaviorRecognition(object):

    def __init__(self, auth):
        self.auth = auth
        self.host = config.get_default('default_requet_host')
        self.api_version = config.get_default('default_api_version')
        self.base_url = 'http://{0}'.format(self.host)
        self.content_type = 'application%2Fjson'

    def device_behavior_recognition(self, reqbody):
        '''

        :param reqbody:
        :return:
        '''
        method = 'POST'
        path = self.api_version + '/driver_behavior'

        if not isinstance(reqbody, dict):
            raise ValueError('Reqeust Body is a dict [%s] ', str(_drive_behavior_body_feild))

        data = reqbody
        headers = {
            'host': self.host,
            'content-type': self.content_type
        }

        authorization = self.auth.get_sign(http_method=method, path=path, params=None, headers=headers)
        url = '{0}{1}'.format(self.base_url, path)
        print(url)
        ret, info = dohttp._post(url, json.dumps(data), authorization, headers=headers)

        return ret, info
