#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    : recognition_machine.py
@Time    : 2019/7/22 11:31
@Author  : caeser zheng
@Email   : zgl3010@qq.com
"""

import json
from horizon import dohttp
import horizon.auth as au
import horizon.services.iServices.facesets as facesets

_user_face_list_feild = set([
    'face_id',  # string	是	用户id,全局唯一,命名规则：仅支持数字，大小写字母，下划线组成，长度限制1-30字符
    'face_name',  # string	是	用户名称, 用户名称，所有所输入字符，有效长度１-48字符，并且不超过64字节
    'ext１',  # string	否	扩展字段１，具体意义由调用者确定
    'ext２',  # string	否	扩展字段２，具体意义由调用者确定
    'ext３',  # string	否	扩展字段３，具体意义由调用者确定
    'ext４',  # string	否	扩展字段４，具体意义由调用者确定
    'ext５',  # string	否	扩展字段５，具体意义由调用者确定
    'image_base64',  # base64	string	是	base64格式编码图片
])

_device_list_feild = set([
    'device_sn',  # string	是	需要绑定的IPC编号
    'threshold',  # string	否	绑定到该IPC上的人脸库的阈值
])


class RecognitionMachineManager(facesets.FaceSetsManager):
    '''
    人脸库管理API可以用于对IPC上的人脸库进行增删改查操作
    '''

    def __init__(self, auth):
        self.auth = auth
        self.host = "recopenapi-aiot.horizon.ai"
        self.api_version = 'openapi/v1'
        self.base_url = 'http://{0}/{1}'.format(self.host, self.api_version)
        self.content_type = 'application%2Fjson'

        self.facesets = facesets.FaceSetsManager(self.auth)


    def faceset_build(self, name):
        '''
        OpenAPI获取创建人脸库指令，内部创建空照片库，返回本次操作的状态码与错误信息
        :param name:string	是	人脸库名称,允许中文，数字、大小写字母、下划线组成，长度限制1-16字符
        :return:
        '''

        method = 'POST'
        path = '/facesets'

        data = {'name': name}

        headers = {
            'host': self.host,
            'content-type': self.content_type
        }

        authorization = self.auth.get_sign(http_method=method, path=path, params=None, headers=headers)
        # url = 'http://{0}{1}?authorization={2}'.format(self.host, path, authorization)
        url = '{0}{1}'.format(self.base_url, path)
        print(url)
        ret, info = dohttp._post(url, json.dumps(data), authorization, headers=headers)

        return ret, info

    def faceset_delete(self, faceset_id):
        '''
        OpenAPI获取删除人脸库指令，删除人脸库，返回状态码与错误信息。
        人脸库删除前，必须先解除该人脸库与所有IPC的绑定关系。存在绑定关系的人脸库，删除会返回错误。
        :param faceset_id:
        :return:
        '''

        method = 'DELETE'
        path = '/facesets/%s' % faceset_id

        headers = {
            'host': self.host
        }

        authorization = self.auth.get_sign(http_method=method, path=path, params=None, headers=headers)
        url = '{0}{1}'.format(self.base_url, path)
        print(url)

        ret, info = dohttp._delete(url, auth=authorization)

        return ret, info

    def user_register(self, faceset_id, face_list):
        '''
        OpenAPI 注册用户接口，内部对指定人脸库注册用户并异步注册给绑定的IPC。返回本次操作的操作id，状态码与错误信息。
        注册用户操作为批量操作，一次最多输入10个用户。每个用户只支持1 张照片，照片为Base64形式编码。
        :param faceset_id:
        :param face_list:
        :return:
        '''
        method = 'POST'
        path = '/facesets/%s/faces' % faceset_id

        if not isinstance(face_list, tuple):
            raise ValueError('face_list must be a arry')
        data = {'face_list': face_list}

        headers = {
            'host': self.host,
            'content-type': self.content_type
        }

        authorization = self.auth.get_sign(http_method=method, path=path, params=None, headers=headers)
        url = '{0}{1}'.format(self.base_url, path)
        print(url)
        ret, info = dohttp._post(url, json.dumps(data), authorization, headers=headers)

        return ret, info

    def user_faces_update(self, faceset_id, face_id, **kwargs):
        '''
        OpenAPI获取更新用户指令，内部对人脸库内用户信息（图片或附加信息）进行更新，
        返回本次操作的操作id，状态码与错误信息。
        :param faceset_id:
        :param face_id:
        :param kwargs:
        :return:
        '''
        method = 'PUT'
        path = '/facesets/{0}/faces/{1}'.format(faceset_id, face_id)

        data = {}
        for k, v in kwargs.items():
            if k in _user_face_list_feild:
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

    def user_faces_delete(self, faceset_id, face_list):
        '''

        :param faceset_id:
        :param face_list:   array	是	用户id列表, string数组
        :return:
        '''
        method = 'DELETE'
        path = '/facesets/%s/faces' % faceset_id

        headers = {
            'host': self.host,
            'content-type': self.content_type
        }

        data = {'face_list': face_list}

        authorization = self.auth.get_sign(http_method=method, path=path, params=None, headers=headers)
        url = '{0}{1}'.format(self.base_url, path)
        print(url)

        ret, info = dohttp._delete(url, data=json.dumps(data), auth=authorization, headers=headers)

        return ret, info

    def user_info_get(self, faceset_id, per_page=1, current=20, **kwargs):
        '''
        OpenAPI获取用户查询指令，内部对指定人脸库查询用户，返回本次操作的用户信息，状态码与错误信息
        :param faceset_id:
        :param face_id:
        :param kwargs:
        :return:
        '''
        method = 'GET'
        path = '/facesets/{0}/faces'.format(faceset_id)

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

        for k, v in kwargs.items():
            if k in _user_face_list_feild:
                params.update({k, v})

        authorization = self.auth.get_sign(http_method=method, path=path, params=params, headers=headers)

        url = '{0}{1}?{2}'.format(
            self.base_url, path, au.get_canonical_querystring(params=params)
        )
        print(url)

        ret, info = dohttp._get(url, '', auth=authorization)
        # 枚举列表是否完整
        eof = False
        if ret:
            if ret["pagination"]["current"] * ret["pagination"]["per_page"] >= ret["pagination"]["total"]:
                eof = True

        return ret, info, eof

    def faceset_ipc_bind(self, faceset_id, device_list):
        '''
        OpenAPI获取绑定人脸库和IPC的指令，内部建立人脸库与IPC的关联关系，并将人脸库数据同步至IPC，返回本次操作的操作id，状态码与错误信息。
        绑定时可以设定IPC 人脸库阈值，可选，默认值为0.74，有效范围为(0.0，1.0）。重复绑定人脸库会返回错误
        :param faceset_id:
        :param device_list:
        :return:
        '''
        method = 'POST'
        path = '/facesets/%s/bind' % faceset_id

        if not isinstance(device_list, tuple):
            raise ValueError('device_list is a arry[{"device_sn":xx,"threshold":xx}]')

        data = {
            'device_list': device_list
        }

        headers = {
            'host': self.host,
            'content-type': self.content_type
        }

        authorization = self.auth.get_sign(http_method=method, path=path, params=None, headers=headers)
        url = '{0}{1}'.format(self.base_url, path)
        print(url)

        ret, info = dohttp._post(url, data=json.dumps(data), auth=authorization, headers=headers)

        return ret, info

    def faceset_ipc_unbind(self, faceset_id, device_list):
        '''

        :param faceset_id:
        :param device_list:
        :return:
        '''
        method = 'DELETE'
        path = '/facesets/%s/unbind' % faceset_id

        if not isinstance(device_list, tuple):
            raise ValueError('device_list is a arry[{"device_sn":xx,"threshold":xx}]')

        headers = {
            'host': self.host,
            'content-type': self.content_type
        }

        data = {'device_list': device_list}

        authorization = self.auth.get_sign(http_method=method, path=path, params=None, headers=headers)
        url = '{0}{1}'.format(self.base_url, path)
        print(url)

        ret, info = dohttp._delete(url, data=json.dumps(data), auth=authorization, headers=headers)

        return ret, info

    def facest_list(self, current=1, per_page=20):
        '''

        :param current:
        :param per_page:
        :return:
        '''
        method = 'GET'
        path = '/facesets'

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

        url = '{0}{1}?{2}'.format(
            self.base_url, path, au.get_canonical_querystring(params=params)
        )
        print(url)

        ret, info = dohttp._get(url, '', auth=authorization)
        # 枚举列表是否完整
        eof = False
        if ret:
            if ret["pagination"]["current"] * ret["pagination"]["per_page"] >= ret["pagination"]["total"]:
                eof = True

        return ret, info, eof

    def ipc_list(self, type, current=1, per_page=20, ):
        '''
        OpenAPI获取设备列表指令，返回的设备类型支持客流识别机与识别机两种类型，客流识别机类型为２，识别机类型为３，
        返回所有IPC信息（包含IPC SN等信息），本次操作的状态码与错误信息
        :param current:
        :param per_page:
        :param type:设备类型，只能是客流识别机(2)或者识别机(3)
        :return:
        '''
        method = 'GET'
        path = '/devices'

        if not type in [2, 3]:
            raise ValueError('type 客流识别机(2)或者识别机(3)')

        # 验证current 、per_page
        if (current and per_page):
            current = current
            per_page = per_page
        elif not (current == per_page):
            raise ValueError('current and per_page must fill in at the same time or neither')

        params = {
            'type': type,
            'current': current,
            'per_page': per_page,
        }

        headers = {
            'host': self.host
        }

        authorization = self.auth.get_sign(http_method=method, path=path, params=params, headers=headers)

        url = '{0}{1}?{2}'.format(
            self.base_url, path, au.get_canonical_querystring(params=params)
        )
        print(url)

        ret, info = dohttp._get(url, '', auth=authorization)
        # 枚举列表是否完整
        eof = False
        if ret:
            if ret["pagination"]["current"] * ret["pagination"]["per_page"] >= ret["pagination"]["total"]:
                eof = True

        return ret, info, eof

    def faceset_ipc_sync(self, faceset_id, face_id, device_sn):
        '''
        OpenAPI获取同步IPC人脸库用户指令，内部依据云端人脸库用户数据同步至IPC人脸库，如云端人脸库不存在用户id，则删除IPC内此用户数据。
        返回本次操作的操作id，状态码与错误信息
        :param faceset_id:
        :param face_id:
        :return:
        '''
        method = 'POST'
        path = '/facesets/%s/faces/%s/sync' % (faceset_id, face_id)

        data = {
            'device_sn': device_sn
        }

        headers = {
            'host': self.host,
            'content-type': self.content_type
        }

        authorization = self.auth.get_sign(http_method=method, path=path, params=None, headers=headers)
        url = '{0}{1}'.format(self.base_url, path)
        print(url)

        ret, info = dohttp._post(url, data=json.dumps(data), auth=authorization, headers=headers)

        return ret, info

    def faceset_ipc_threshold_modify(self, faceset_id, device_sn, threshold):
        '''
        OpenAPI获取修改IPC人脸库阈值指令，内部更新IPC人脸库阈值，返回本次操作的操作id，状态码与错误信息
        :param faceset_id:
        :param device_sn:
        :param threshold:
        :return:
        '''
        method = 'PUT'
        path = '/facesets/%s/threshold' % (faceset_id)

        data = {
            'device_sn': device_sn,
            'threshold':threshold
        }

        headers = {
            'host': self.host,
            'content-type': self.content_type
        }

        authorization = self.auth.get_sign(http_method=method, path=path, params=None, headers=headers)
        url = '{0}{1}'.format(self.base_url, path)
        print(url)

        ret, info = dohttp._put(url, data=json.dumps(data), auth=authorization, headers=headers)

        return ret, info

    def operations_search(self,request_id,faceset_id):
        '''
        返回操作id对应的结果。结果内包含与faceset_id关联所有IPC的未成功的face_id状态信息。
        未成功状态包括pending和fail。
        已成功的face_id，不在查询结果中。
        :param request_id:
        :param faceset_id:
        :return:
        '''
        method = 'GET'
        path = '/operations/%s' % request_id

        params = {
            'faceset_id':faceset_id
        }

        headers = {
            'host': self.host
        }

        authorization = self.auth.get_sign(http_method=method, path=path, params=params, headers=headers)
        url = '{0}{1}?{2}'.format(self.base_url, path,au.get_canonical_querystring(params))
        print(url)
        ret, info = dohttp._get(url, auth=authorization)

        return ret, info
