#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    : test_facesets.py
@Time    : 2019/7/18 14:54
@Author  : caeser zheng
@Email   : zgl3010@qq.com
"""

from horizon.services.iServices import behaviorRec
from horizon.auth import Auth
import unittest
import json
import sys
from horizon.example.utils import HorizionTestBase
from horizon.example.test_param_cfg import ak, sk


class DriveBehaviorRecognitionTest(HorizionTestBase):

    def test_fdb_drive_behavior_recognition(self, fdb):
        image_url_set = ['http://z-qn-oss.ultrakevin.top/horizion/test/mp4-00000'+str(x)+'.mp4' for x in range(0,9)]

        for url in image_url_set:
            body = {
                'video_type':url
            }
            re = fdb.device_behavior_recognition(body)

            op = 'test %s ' % sys._getframe().f_code.co_name
            self.writelog(re, op)


if __name__ == '__main__':
    mac = Auth(ak, sk)
    fdb = behaviorRec.DriveBehaviorRecognition(mac)

    ht = DriveBehaviorRecognitionTest(log_path='../../log', log_tag='iService',log_file='behavior')
    #ht.test_fdb_detect(fdb)
    ht.test_fdb_drive_behavior_recognition(fdb)
    #ht.test_fdb_face_search(fdb)
    #ht.test_fdb_face_match(fdb)
