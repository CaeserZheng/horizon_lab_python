#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    : test.py.py
@Time    : 2019/7/16 18:29
@Author  : caeser zheng
@Email   : zgl3010@qq.com
"""
#from horizon_lab_python.horizon.auth import Auth
from horizon.auth import Auth
from horizon.services.device.manager import deviceSpaceManager
import qiniu

ak = 'J1dKGVvbsU7bciqUk0vkC7UB'
sk = 'PrjvA7hWOQojtgt2PYYWkgFXu7bYXnPw'

http_method = 'POST'
path = '/test/'
params = {
    'a':1,
    'b':2
}
header = {'content-type': 'application/x-www-form-urlencoded'}

if __name__ == '__main__':
    mac = Auth(ak, sk)
    print(mac.get_sign(http_method, path, params, header))

    dm = deviceSpaceManager(mac)
    dm.list()

