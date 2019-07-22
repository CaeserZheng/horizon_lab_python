#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    : faceu.py
@Time    : 2019/7/18 14:23
@Author  : caeser zheng
@Email   : zgl3010@qq.com
"""

import json
from horizon import dohttp
import horizon.auth as au

_face_user_register_feild = set([
    'attributes',  # 用户属性
    'images',  # 注册图片列表，最少1张，最多5张
    'model_version',  # 模型版本，当存在用特征进行添加时，此为必需字
    'encryption',  # 0表示未加密，1表示加密，当存在用特征进行添加时，此为必需字段
    'shift_l'  # sln变换需要的参数，有效范围[0,32)，当这个字段不存在时，认为特征的值base64解码后是float组成的字符串，否则认为是int组成的字符串且将做变换
])

_face_attributes_feild = set([
    'age',  # int	否	用户年龄
    'gender'  # string	否	用户性别，分为female/male/unkno
])

_face_images_field = set([
    'image_type',  # 0: 通过url识别，参数image_url不为空；1: 通过图片image_base64识别，参数image_base64不为空
    'image_url',  # 输入图片URL
    'image_base64',  # 图片二进制的base64值
    'features'  # 第二张图的特征的base64字符串。将每一维特征的值按照相应的类型转为字符串并以逗号为分隔符进行拼接，拼接后整体进行base64
])


class FaceUserManager(object):
    '''
    人脸库的用户管理API可用于对特定人脸库中的用户进行注册、删除、原信息更改、人脸更新，以及用户列表的查询。
    注意：在调用人脸库用户管理API之前，需要确保该人脸库已经存在
    '''

    def __init__(self, auth):
        self.auth = auth
        self.host = "api-aiot.horizon.ai"
        self.api_version = '/openapi/v1'
        self.base_url = 'http://{0}'.format(self.host)
        self.content_type = 'application%2Fjson'

    def register(self, faceset_id, images, **kwargs):
        '''
        用于向人脸库中新增用户
        :param faceset_id:
        :param kwargs:
        :return:
        '''

        method = 'POST'
        path =self.api_version + '/facesets/%s/faces' % faceset_id

        data = {'images': images}
        for k, v in kwargs.items():
            if k in _face_user_register_feild:
                data.update({k: v})
            else:
                raise ValueError('error param [%s]' % k)

        headers = {
            'host': self.host,
            'content-type': self.content_type
        }

        authorization = self.auth.get_sign(http_method=method, path=path, params=None, headers=headers)
        url = '{0}{1}'.format(self.base_url, path)
        print(url)
        ret, info = dohttp._post(url, json.dumps(data), authorization, headers=headers)

        return ret, info

    def delete(self, faceset_id, face_id):
        '''
        删除当前api调用者指定的人脸库
        :param face_id:
        :return:
        '''
        method = 'DELETE'
        path =self.api_version + '/facesets/{0}/faces/{1}'.format(faceset_id, face_id)

        headers = {
            'host': self.host
        }

        authorization = self.auth.get_sign(http_method=method, path=path, params=None, headers=headers)

        # url = 'http://{0}{1}?authorization={2}'.format(self.host, path, authorization)
        url = '{0}{1}'.format(self.base_url, path)
        print(url)

        ret, info = dohttp._delete(url, auth=authorization)

        return ret, info

    def update_user(self, faceset_id, face_id, **kwargs):
        '''
        用于对人脸库中指定的用户，更新其信息，目前仅支持人脸特征照片、性别和年龄段
        :param faceset_id:
        :param face_id:
        :return:
        '''
        method = 'PUT'
        path =self.api_version + '/facesets/{0}/faces/{1}'.format(faceset_id, face_id)

        data = {}
        for k, v in kwargs.items():
            if k in _face_user_register_feild:
                data.update({k: v})

        headers = {
            'host': self.host,
            'conent-type': self.content_type
        }

        authorization = self.auth.get_sign(http_method=method, path=path, params=None, headers=headers)

        url = '{0}{1}'.format(self.base_url, path)
        print(url)

        ret, info = dohttp._put(url, data=json.dumps(data), auth=authorization, headers=headers)

        return ret, info

    def update_user_image(self, faceset_id, face_id, images, **kwargs):
        '''
        用于向人脸库中指定用户添加人脸特征图片
        :param faceset_id:
        :param face_id:
        :param images:


        :return:
        '''
        method = 'POST'
        path =self.api_version + '/facesets/%s/faces/%s/images_add' % (faceset_id, face_id)

        data = {'images': images}
        for k, v in kwargs.items():
            if k in _face_user_register_feild:
                data.update({k: v})

        headers = {
            'host': self.host,
            'conent-type': self.content_type
        }

        authorization = self.auth.get_sign(http_method=method, path=path, params=None, headers=headers)

        url = '{0}{1}'.format(self.base_url, path)
        print(url)

        ret, info = dohttp._post(url, data=json.dumps(data), auth=authorization, headers=headers)

        return ret, info

    def search(self, faceset_id, face_id):
        '''
        用于获取一个用户的信息，包括注册使用照片，年龄段、性别
        :param faceset_id:
        :return:
        '''
        method = 'GET'
        path =self.api_version + '/facesets/{0}/faces/{1}'.format(faceset_id, face_id)

        headers = {
            'host': self.host
        }

        authorization = self.auth.get_sign(http_method=method, path=path, params=None, headers=headers)
        url = '{0}{1}'.format(self.base_url, path)
        print(url)

        ret, info = dohttp._get(url, auth=authorization)

        return ret, info

    def list(self, faceset_id, current=1, per_page=20):
        '''
        用于获取指定人脸库中的用户列表,单个人脸库可注册的用户最大的数据量是100万,超过100万会报错
        参考：https://iotdoc.horizon.ai/busiopenapi/part4_api_basic/faceset_face.html#part4_1_4
        :param current:当前页,不填时默认为1，需要和per_page同时填/不填
        :param per_page:每页数量，不填时默认值为20
        :param faceset_id:设备空间id，不传时返回默认设备空间下的设备列表
        :return:
            一个dict变量，类似 {"hash": "<Hash string>", "key": "<Key string>"}
            一个ResponseInfo对象
            一个EOF信息。
        '''

        method = 'GET'
        path =self.api_version + '/facesets/%s/faces' % faceset_id

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

        url = '{0}{1}?{2}'.format(
            self.base_url, path, query
        )
        print(url)

        ret, info = dohttp._get(url, '', auth=authorization)
        # 枚举列表是否完整
        eof = False
        if ret:
            if ret["pagination"]["current"] * ret["pagination"]["per_page"] >= ret["pagination"]["total"]:
                eof = True

        return ret, info, eof
