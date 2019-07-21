#!/usr/bin/env python
#-.- coding=utf-8 -.-
'''
__author__ = 'caeser'
__mtime__ = '2019/7/18'
'''

from horizon.services.iDevices import device, passengerflow, space
from horizon.auth import Auth
import unittest
import json
from horizon.test.utils  import HorizionTestBase
from horizon.test.test_param_cfg import ak,sk
import sys



class PassengerFlowTest(HorizionTestBase):

    def test_pf_line_config(self,fdb):
        device_sn = 'xxxx'
        line_type=1
        point = {
            "top_left_x": 1656,
            "top_left_y": 415,
            "bottom_right_x": 271,
            "bottom_right_y": 408
        }
        lines = [
            {
                'line_type':line_type,
                'point':point
            }
        ]
        start_time = '08:00:00'
        end_time = '23:00:00'

        re = fdb.pf_line_config(device_sn = device_sn,lines = lines,start_time=start_time,end_time=end_time)

        op = 'test %s ' % sys._getframe().f_code.co_name
        self.writelog(re,op)


    def test_pf_line_search(self,fdb):
        device_sn = 'xxxx'

        op = 'test %s ' % sys._getframe().f_code.co_name
        re = fdb.pf_line_search(device_sn=device_sn)

        self.writelog(re, op)
    def test_pf_line_switch(self,fdb):
        device_sn = 'xxxx'
        switch_status = 1

        op = 'test %s ' % sys._getframe().f_code.co_name
        re = fdb.pf_line_switch(device_sn=device_sn,switch_status=switch_status)

        self.writelog(re, op)

    def test_pf_line_delete(self,fdb):
        device_sn = 'xxxx'

        op = 'test %s ' % sys._getframe().f_code.co_name
        re = fdb.pf_line_delete(device_sn=device_sn)

        self.writelog(re,op)


if __name__ == '__main__':

    mac = Auth(ak,sk)
    fdb = passengerflow.PassengerFlowManager(mac)

    ht = PassengerFlowTest(log_path='../../log',log_tag='deviceManeger_passengerflow')

    #####test space.py
    #ht.test_pf_line_config(fdb=fdb)
    #ht.test_pf_line_search(fdb=fdb)
    ht.test_pf_line_switch(fdb=fdb)
    ht.test_pf_line_delete(fdb=fdb)