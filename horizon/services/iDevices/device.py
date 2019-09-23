#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    : device.py
@Time    : 2019/7/17 16:02
@Author  : caeser zheng
@Email   : zgl3010@qq.com
"""

import json
from horizon import dohttp
import horizon.auth as au
from horizon.config import _config

_moduls_feild = set([
        'capture_config',  #摄像机配置模块
])
_device_info_feild = set([
    'space_id',	    #string	是	目标设备空间id
    'name',	        #string	否	设备名称，长度限制80字节
    'position',	    #string	否	设备所在设备空间具体位置，长度限制80字节
    'description',	#string	否	设备描述,长度限制512字节
    'extra'	        #string	否	设备额外信息，长度限制512字节
])
_capture_config_feild = set([
    'snapsizethr',	#int	抓拍的最小人脸大小(单位像素)，抓拍机/客流机：32~256；识别机：64~256，默认值：80
    'frontthr', 	#int	抓拍阀值，取值：1~10；对应值：1--(-2000)；2--(-1000)；3--(0)；4--(500)；5--(1000)；6--(1200)；7--(1400)；8--(1600)；9--(1700)；10--(1800)，默认值：5
    'beginpostframethr',	#int	目标抓拍时间，取值：[0.5、1、2、3、4、5、10、20、30、40]；对应值：0.5--10; 1--25; 2--50; 3--75; 4--100; 5--125; 10--250; 20--500; 30--750; 40--1000，默认值：20
    'snapscale',	#double 人脸外廓系数，有效范围：1.0~4.0，默认值：1.6000000238418579
    'resnapthr',	#int	再次抓取时间差，需要大于目标抓拍时间（beginpostframethr）参数的值，否则设置不生效，设置为1表示再次抓拍设置无效，取值：[0、0.5、1、2、3、4、5、10、20、30、40]，对应值：0--1； 0.5--10； 1--25；2--50; 3--75; 4--100; 5--125; 10--250; 20--500; 30--750; 40--1000
    'firstnumavailthr',	#int	单个track ID抓拍图片数，有效范围：1~3，默认值：1
    'numaftervanish',	#int	track ID消失帧数，有效范围：1~100，默认值：50
    'switchregion',	    #boolean	是否仅在指定区域中抓拍，有效范围：false、true，默认值：false
    'captregion',    	#array	抓拍区域坐标，有效范围：0~1920、0~1080，默认值：[{"x1":0,"y1":0,"x2":1920,"y2":1080,"id":0,"type":0}]
    'captbackground',	#boolean	是否抓拍人脸出现时的背景图，有效范围：true、false，默认值：false
    'track_score_eliminate',	#int	灵敏度，设置值范围：1~10, 对应值：1--70；2--66；3--64；4--63；5--62；6--61；7--60；8--59；9--58；10--57，默认值：5
    'snap_mode'	    #int	开关，是否开启全量抓拍，有效范围：0~1，默认值：0
])


class DeviceManager(object):
    '''
    设备空间管理
    '''

    def __init__(self,auth):
        self.auth = auth
        self.host = _config['default_requet_host']
        self.api_version = _config['default_api_version']
        self.base_url = 'http://{0}'.format(self.host)

        self.content_type = 'application%2Fjson'

    def list(self,current=1,per_page=20,space_id=None,attributes=None):
        '''
        获取设备空间列表
        参考：https://iotdoc.horizon.ai/busiopenapi/part1_device_space/device_space.html#part1_0
        :param current:当前页,不填时默认为1，需要和per_page同时填/不填
        :param per_page:每页数量，不填时默认值为20
        :param space_id:设备空间id，不传时返回默认设备空间下的设备列表
        :param attributes:用户自定义获取信息字段，如果不传则默认返回设备通用信息，
        attributes={name,capture_config}
            name          模块
            capture_config 配置
        :return:
            一个dict变量，类似 {"hash": "<Hash string>", "key": "<Key string>"}
            一个ResponseInfo对象
            一个EOF信息。
        '''

        method = 'GET'
        path =self.api_version + '/devices'

        #验证current 、per_page
        if  (current and per_page):
            current = current
            per_page = per_page
        elif not (current == per_page):
            raise ValueError('current and per_page must fill in at the same time or neither')

        #生成请求参数
        params = {
            'current': current,
            'per_page' : per_page,
        }
        params.update({'space_id':space_id}) if space_id else None
        if attributes:
            params.update({'attributes': 'capture_config'})
            params.update({'capture_config': attributes['capture_config']})

        headers = {
            'host' : self.host
        }

        authorization = self.auth.get_sign(http_method=method,path=path,params=params,headers=headers)

        url = '{0}{1}?{2}'.format(
            self.base_url, path, au.get_canonical_querystring(params=params)
        )
        print(url)

        ret, info = dohttp._get(url, '',auth=authorization)
        # 枚举列表是否完整
        eof = False
        if ret :
            if ret["pagination"]["current"] * ret["pagination"]["per_page"] >= ret["pagination"]["total"]:
                eof = True

        return ret, info, eof

    def device_info(self,device_sn,attributes=None):
        '''
        返回指定的设备空间详细信息,主要是设备空间本身的属性信息
        :param device_sn: 空间id
        :param attributes: 用户自定义获取信息字段，如果不传则默认返回设备通用信息
        :return:
        '''

        method = 'GET'
        path =self.api_version + '/devices/%s' % device_sn

        params = {}

        if attributes:
            params.update({'attributes': 'capture_config'})
            params.update({'capture_config': attributes['capture_config']})

        headers = {
            'host': self.host
        }

        authorization = self.auth.get_sign(http_method=method, path=path, params=params, headers=headers)

        if params:
            url = '{0}{1}?{2}'.format(self.base_url, path,au.get_canonical_querystring(params))
        else:
            url = '{0}{1}'.format(self.base_url,path)
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
        path =self.api_version + '/devices/%s/update' % device_sn

        data = {'space_id':space_id}
        for k,v in kwargs.items():
            data.update({k:v}) if k in _device_info_feild else None


        headers = {
            'host': self.host,
            'content-type': self.content_type
        }

        authorization = self.auth.get_sign(http_method=method, path=path, params=None, headers=headers)
        url = '{0}{1}'.format(self.base_url, path)
        print(url)

        ret, info = dohttp._put(url, json.dumps(data), authorization, headers=headers)

        return ret, info

    def update_config(self,device_sn,device_cfg):
        '''
        更改设备绑定的设备空间，以及设备位置等元信息；
        当更换设备的设备空间时，该接口是异步接口，可根据返回值的request_id请求获取异步任务状态接口获取请求状态
        :param device_sn:设备编号

        kwargs:
        module	Array	是	设备配置模块，详见module说明（设备配置参数下发）

        module 说明：
        name	string	是	模块名称,可配置的名称详见module可配置名称说明（设备配置参数下发）
        parm	Array	是	模块参数配置数组，详见parm说明（设备配置参数下发）

        "module":[{
            "name":"capture_config",
            "parm":[
                {
                    "name":"aaa",
                    "value":"aaa"
                },
                {
                    "name":"bbb",
                    "value":"bbb"
                }
            ]
        }]
        '''

        method = 'PUT'
        path =self.api_version + '/devices/%s' % device_sn

        moduls = 'capture_config'
        if isinstance(device_cfg, list):
            params = [device_cfg]
        else:
            raise ValueError('device_cfg must be a list')

        data = {
            'moduls': [{
                'name': moduls,
                'parm': params
            }]
        }

        headers = {
            'host': self.host,
            'content-type': self.content_type
        }

        authorization = self.auth.get_sign(http_method=method, path=path, params=None, headers=headers)
        url = '{0}{1}'.format(self.base_url, path)
        print(url)
        ret, info = dohttp._put(url, json.dumps(data), authorization, headers=headers)
        return ret, info

    def screenshot(self,device_sn):
        '''
        获取指定设备预览图,该接口是一个异步接口，若要获取最新的结果，需要根据返回的request_id调用获取异步请求状态获取
        :param device_sn:
        :return:
        '''
        method = 'POST'
        path =self.api_version + '/devices/screenshot'

        data = {
            'device_sn':device_sn
        }

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

    def device_delete(self,device_sn):
        '''
        从指定设备空间移除设备,设备会回退到默认设备空间；接口是异步接口，可根据返回值的request_id请求获取异步任务状态接口获取请求状态
        :param device_sn:
        :return:
        '''
        method = 'DELETE'
        path =self.api_version + '/devices/%s' % device_sn

        headers = {
            'host': self.host
        }

        authorization = self.auth.get_sign(http_method=method, path=path, params=None, headers=headers)
        url = '{0}{1}'.format(self.base_url, path)
        print(url)
        ret, info = dohttp._delete(url, auth=authorization)
        return ret, info

    def reqest_stat(self,device_sn,request_id):
        '''
        获取指定异步请求的执行状态，包括配置下发、客流画线、画域、修改阈值等异步接口
        :param device_sn:
        :param request_id:
        :return:
        '''
        pass

