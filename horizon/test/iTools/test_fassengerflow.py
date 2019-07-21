#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    : test_facesets.py
@Time    : 2019/7/18 14:54
@Author  : caeser zheng
@Email   : zgl3010@qq.com
"""

from horizon.services.iTools import passengerflow
from horizon.auth import Auth
import unittest
import json,sys
from horizon.test.utils import HorizionTestBase
from horizon.test.test_param_cfg import ak, sk
from horizon.utils import image_base64_encode, image_base64_decode
import time


class PassengerFlowTest(HorizionTestBase):

    def test_fdb_enable_analysis(self,fdb):
        space_id = 'a21c33f35d2d88ad0dac680b_S5goKvFq'

        op = 'test %s ' % sys._getframe().f_code.co_name
        re = fdb.enable_analysis(space_id=space_id)
        self.writelog(re , op)

    def test_fdb_attach_facesets_to_space(self,fdb):
        space_ids = ['a21c33f35d2d88ad0dac680b_S5goKvFq',]
        faceset_ids = ['5d349b58f67f1000085b21fe',]

        re = fdb.attach_facesets_to_space(space_ids=space_ids,faceset_ids=faceset_ids)
        op = 'test %s ' % sys._getframe().f_code.co_name
        self.writelog(re , op)

    def test_fdb_visitors_sub(self,fdb):
        topic_name ='space'
        topic_id ='a21c33f35d2d88ad0dac680b_S5goKvFq'
        client_id = 'visitor_sub_space_1'

        re = fdb.visitors_sub(topic_name=topic_name , topic_id=topic_id,client_id=client_id)
        op = 'test %s ' % sys._getframe().f_code.co_name
        self.writelog(re , op)




if __name__ == '__main__':
    mac = Auth(ak, sk)
    fdb = passengerflow.PassergentFlowAnalysis(mac)

    ht = PassengerFlowTest(log_path='../../log', log_tag='iTools_passengerflow')

    #ht.test_fdb_enable_analysis(fdb)
    #ht.test_fdb_attach_facesets_to_space(fdb)
    ht.test_fdb_visitors_sub(fdb)
