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
from horizon.services.deviceManager.space import deviceSpaceManager
from horizon.services.deviceManager.device import deviceManager
import urllib

ak = 'J1dKGVvbsU7bciqUk0vkC7UB'
sk = 'PrjvA7hWOQojtgt2PYYWkgFXu7bYXnPw'


if __name__ == '__main__':
    mac = Auth(ak, sk)
    #print(mac.get_sign(http_method, path, params, header))

    dm = deviceManager(mac)
    #test device list
    current = 1
    per_page = 1
    attributes = {
        'capture_config':['snapsizethr','frontthr']
    }
    print(dm.list(current,per_page,attributes))

    device_sn='fadfadf'
    #print(dm.device_info(device_sn))

    space_id = 'a21c33f35d2d88ad0dac680b_FKmwSD3s'
    #print(dm.update_info("aaaa",space_id,name="aaa"))

    dsm = deviceSpaceManager(mac)
    # test update deviceManager space
    print('test update deviceManager space')
    name = 'ipc_testtt'
    des = 'aaaaa'
    space_id = 'a21c33f35d2d88ad0dac680b_FKmwSD3s'
    #print(dsm.update(space_id,name=name,description=des))

    #test make a deviceManager
    name = 'ipc_test5'
    des = '人脸识别3'
    #print(dsm.mkspace(name,description=des))


    #test info
    space_id = 'a21c33f35d2d88ad0dac680b_24MEbzao'
    #print(dsm.space_info(space_id))

    #delete space
    space_id = 'a21c33f35d2d88ad0dac680b_24MEbzao'
    #print(dsm.delete(space_id))



    #test list
    '''
    current = 0
    per_page = 1
    eof = False
    while not eof:
        current += 1
        ret, eof, info = dsm.list(current, 1)
        print("#page-%d" % current)
        print(ret)
        print("\n")
    '''



