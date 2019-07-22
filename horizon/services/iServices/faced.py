#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    : faced.py
@Time    : 2019/7/18 14:24
@Author  : caeser zheng
@Email   : zgl3010@qq.com
"""
import json
from horizon import dohttp
import horizon.auth as au
import re

_face_detect_feild = set([
    'image_type',  # int	是	0: 通过url识别，参数image_url不为空；1: 通过图片image_base64识别，参数image_base64不为空
    'image_url',  # string	否	输入图片URL
    'image_base64',  # string	否	图片二进制的base64值
    'max_face_count',  # int	否	最大检测的人脸数，默认为1,最大值为100
    'keypoint',  # boolean	否	当传入字段为true时，每个图片返回包含关键点，默认为false
    'quality',  # boolean	否	当传入字段为true时，每个图片返回图片质量，默认为false
    'attributes',  # string	否	当需要检测的一些属性信息时传入此字段；当前支持的属性有pose,age,gender,feature；多个属性用逗号隔开
    'face_rect',
    # string	否	指定人脸框位置提取特征，4个int类型，依次是左上角横坐标，左上角纵坐标，右下角横坐标，右下角纵坐标； 比如： "face_rect": "24,19,74,83"。不提供此参数时，默认检测当前图片的最大人脸；当传入此参数时，对于此人脸框之外的区域，系统不会进行人脸检测，也不会返回任何其他的人脸信息
])

_face_match_feild = set([
    'image_type',  # int	是	0: 通过url识别，参数image_url不为空；1: 通过图片image_base64识别，参数image_base64不为空
    'image_url_1',  # string	否	第一张图片URL
    'image_url_2',  # string	否	第二张图片URL
    'image_base64_1',  # string	否	第一张图片的base64 编码的二进制图片数据
    'image_base64_2',  # string	否	第二张图片的base64 编码的二进制图片数据
    'face_rect_1',
    # string	否	第一张图片指定人脸位置，4个int类型，依次是左上角横坐标，左上角纵坐标，右下角横坐标，右下角纵坐标； 比如： "face_rect_1": "24,19,74,83"。不提供此参数时，默认检测当前图片的最大人脸；当传入此参数时，对于此人脸框之外的区域，系统不会进行人脸检测，也不会返回任何其他的人脸信息
    'face_rect_2',
    # string	否	第二张图片指定人脸位置，4个int类型，依次是左上角横坐标，左上角纵坐标，右下角横坐标，右下角纵坐标； 比如： "face_rect_2": "24,19,74,83"。不提供此参数时，默认检测当前图片的最大人脸；当传入此参数时，对于此人脸框之外的区域，系统不会进行人脸检测，也不会返回任何其他的人脸信息
    'features_1',  # string	否	第一张图的特征的base64字符串。将每一维特征的值按照相应的类型转为字符串并以逗号为分隔符进行拼接，拼接后整体进行base64，当希望用特征进行搜索时，此为必需字段
    'features_2',  # string	否	第二张图的特征的base64字符串。将每一维特征的值按照相应的类型转为字符串并以逗号为分隔符进行拼接，拼接后整体进行base64，当希望用特征进行搜索时，此为必需字段
    'model_version',  # string	否	模型版本，当希望用特征进行比对时，此为必需字段
    'encryption',  # int	否	0表示未加密，1表示加密，当希望用特征进行比对时，此为必需字段
    'shift_l'  # int	否	sln变换需要的参数，有效范围[0,32)，当这个字段不存在时，认为features字段的值base64解码后是float组成的字符串，否则认为是int组成的字符串且将做变换
])

_face_search_feild = set([
    'image_type',  # int	是	0: 通过url识别，参数image_url不为空；1: 通过图片image_base64识别，参数image_base64不为空
    'image_url',  # string	否	输入图片URL
    'image_base64'  # string	否	图片的base64 编码的二进制图片数据
    'faceset_ids',  # array	是	指定需要搜索的人脸库id列表
    'top_n',  # int	否	int类型，返回一个人脸库top_n个最接近待搜索的人脸，最大值10；默认值为10
    'model_version',  # string	否	模型版本，当希望用特征进行搜索时，此为必需字段
    'encryption',  # int	否	0表示未加密，1表示加密，当希望用特征进行搜索时，此为必需字段
    'features',  # string	否	base64字符串，将每一维特征的值按照相应的类型转为字符串并以逗号为分隔符进行拼接，拼接后整体进行base64，当希望用特征进行搜索时，此为必需字段
    'shift_l'  # int	否	sln变换需要的参数，有效范围[0,32)，当这个字段不存在时，认为features字段的值base64解码后是float组成的字符串，否则认为是int组成的字符串且将做变换
])

_face_face_extract_feild = set([
    'image_type',  # int	是	0: 通过url识别，参数image_url不为空；1: 通过图片image_base64识别，参数image_base64不为空
    'image_url',  # string	否	输入图片URL
    'image_base64',  # string	否	图片二进制的base64值
    'max_face_count'  # int	否	最大检测的人脸数，默认为1,最大值为100
])


class FaceDetect(object):
    '''
    人脸识别API可以用于对人脸检测、人脸抠图、人脸的1:1 compare以及1：N search
    '''

    def __init__(self, auth):
        self.auth = auth
        self.host = "api-aiot.horizon.ai"
        self.api_version = 'openapi/v1'
        self.base_url = 'http://{0}/{1}'.format(self.host, self.api_version)
        self.content_type = 'application%2Fjson'

    def __checkurl(self, strs):
        url_pattern = 'https?://[^\s]*'
        return re.match(url_pattern, strs)

    def detect(self, image_type, image_obj, **kwargs):
        '''
        传入图片进行人脸检测和人脸分析
        :param image_type:
        :param kwargs:
        :return:
        '''
        method = 'POST'
        path = '/faces/detect'

        data = {'image_type': image_type}

        if image_type:
            data.update({'image_base64': image_obj})
        else:
            if self.__checkurl(image_obj):
                data.update({'image_url': image_obj})
            else:
                raise ValueError('error image_url [%s..]' % (image_obj[:10]))

        for k, v in kwargs.items():
            if k in _face_detect_feild:
                data.update({k: v})

        headers = {
            'host': self.host,
            'content-type': self.content_type
        }

        authorization = self.auth.get_sign(http_method=method, path=path, params=None, headers=headers)
        url = '{0}{1}'.format(self.base_url, path)
        print(url)
        ret, info = dohttp._post(url, json.dumps(data), authorization, headers=headers)

        return ret, info

    def match(self, image_type, image_obj_1, image_obj_2, **kwargs):
        '''
        将两个人脸进行比对，来判断是否为同一个人
        :param image_type:
        :param image_obj:
        :param kwargs:
        :return:
        '''
        method = 'POST'
        path = '/faces/match'

        data = {'image_type': image_type}

        if image_type:
            data.update({'image_base64_1': image_obj_1})
            data.update({'image_base64_2': image_obj_2})
        else:
            data.update({'image_url_1': image_obj_1})
            data.update({'image_url_2': image_obj_2})

        for k, v in kwargs.items():
            if k in _face_match_feild:
                data.update({k: v})

        headers = {
            'host': self.host,
            'content-type': self.content_type
        }

        authorization = self.auth.get_sign(http_method=method, path=path, params=None, headers=headers)
        url = '{0}{1}'.format(self.base_url, path)
        print(url)
        ret, info = dohttp._post(url, json.dumps(data), authorization, headers=headers)

        return ret, info

    def search(self, image_type, image_obj, faceset_ids, **kwargs):
        '''

        :param image_type:
        :param image_obj:
        :param faceset_ids:
        :param kwargs:
        :return:
        '''
        method = 'POST'
        path = '/faces/search'

        data = {'image_type': image_type}

        if image_type:
            data.update({'image_base64': image_obj})
        else:
            if self.__checkurl(image_obj):
                data.update({'image_url': image_obj})
            else:
                raise ValueError('error image_url [%s..]' % (image_obj[:10]))

        data.update({'faceset_ids': faceset_ids})

        for k, v in kwargs.items():
            if k in _face_search_feild:
                data.update({k: v})

        headers = {
            'host': self.host,
            'content-type': self.content_type
        }

        authorization = self.auth.get_sign(http_method=method, path=path, params=None, headers=headers)
        url = '{0}{1}'.format(self.base_url, path)

        ret, info = dohttp._post(url, json.dumps(data), authorization, headers=headers)

        return ret, info


    def face_extract(self, image_type, image_obj, **kwargs):
        '''
        返回当前上传图片中的人脸图
        :param image_type:
        :param image_obj:
        :param kwargs:
        :return:
        '''
        method = 'POST'
        path = '/faces/face_extract'


        data = {'image_type': image_type}

        if image_type:
            data.update({'image_base64': image_obj})
        else:
            if self.__checkurl(image_obj):
                data.update({'image_url': image_obj})
            else:
                raise ValueError('error image_url [%s..]' % (image_obj[:10]))

        for k, v in kwargs.items():
            if k in _face_face_extract_feild:
                data.update({k: v})

        headers = {
            'host': self.host,
            'content-type': self.content_type
        }

        authorization = self.auth.get_sign(http_method=method, path=path, params=None, headers=headers)
        url = '{0}{1}'.format(self.base_url, path)
        print(url)
        ret, info = dohttp._post(url, json.dumps(data), authorization, headers=headers)

        return ret, info
