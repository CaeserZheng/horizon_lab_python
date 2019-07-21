#!/usr/bin/env python
#-.- coding=utf-8 -.-
'''
__author__ = 'caeser'
__mtime__ = '2019/7/18'
'''

from horizon.services.iDevices import device
from horizon.auth import Auth
import unittest
import json,sys
from horizon.test.utils  import HorizionTestBase
from horizon.test.test_param_cfg import ak,sk



class DeviceTest(HorizionTestBase):

    def test_device_list(self,fdb):
        current = 1
        per_page = 20
        space_id = 'a21c33f35d2d88ad0dac680b_S5goKvFq'
        attributes = {'capture_config': ['snapsizethr', 'frontthr']}

        op = 'test %s ' % sys._getframe().f_code.co_name
        re = fdb.list()

        self.writelog(re,op)

    def test_device_device_info(self,fdb):
        device_sn = 'a21c33f35d2d88ad0dac680bdefaultdevice'
        attributes = {'capture_config':['snapsizethr','frontthr']}

        op = 'test %s ' % sys._getframe().f_code.co_name
        re = fdb.device_info(device_sn,attributes = attributes)

        self.writelog(re,op)

    def test_device_update_info(self,fdb):
        device_sn = 'a21c33f35d2d88ad0dac680bdefaultdevice'
        space_id = 'a21c33f35d2d88ad0dac680b_S5goKvFq'


        name = 'test1'
        position = ''
        description = 'device build 1'
        extra = ''
        op = 'test %s ' % sys._getframe().f_code.co_name

        re = fdb.update_info(device_sn=device_sn,space_id=space_id,name=name)

        self.writelog(re, op)

    def test_device_update_config(self,fdb):
        device_id = 'a21c33f35d2d88ad0dac680b_BQ5KZjor'
        name = 'test_update_device'
        description = 'test update device'
        extra = json.dumps({'enable_analysis_tools':True})

        op = 'test %s ' % sys._getframe().f_code.co_name
        re = fdb.update(device_id=device_id,name=name,description=description,extra=extra)

        self.writelog(re,op)

    def test_device_delete(self, fdb):
        device_id = 'a21c33f35d2d88ad0dac680b_BQ5KZjor'

        op = 'test %s ' % sys._getframe().f_code.co_name
        re = fdb.delete(device_id=device_id)

        self.writelog(re,op)



if __name__ == '__main__':

    mac = Auth(ak,sk)
    fdb = device.DeviceManager(mac)

    ht = DeviceTest(log_path='../../log',log_tag='iDevice_device')

    #####test device.py
    #ht.test_device_list(fdb=fdb)
    ht.test_device_device_info(fdb)
    ht.test_device_update_info(fdb=fdb)