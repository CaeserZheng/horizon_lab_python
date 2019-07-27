#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    : test_facesets.py
@Time    : 2019/7/18 14:54
@Author  : caeser zheng
@Email   : zgl3010@qq.com
"""

from horizon.services.iServices import facedet, facesets, faceu
from horizon.auth import Auth
import unittest
import json
import sys
from horizon.example.utils import HorizionTestBase
from horizon.example.test_param_cfg import ak, sk
from horizon.utils import image_base64_encode


class FaceuTest(HorizionTestBase):

    def test_fdb_register(self, fdb):
        faceset_id = '5d3029a7a21c33000804b8e4'
        attributes = {
            'age': 34,
            'gender': 'male'
        }
        images = []
        image1 = {
            'image_type': 0,
            'image_url': 'http://puptun6bs.bkt.clouddn.com/horizon_faseu/person_career.jpg'
        }
        #images.append(image1)
        #image_file = 'E:\Pictures\james.png'
        image_file = '../../image/wyz_01.jpeg'
        image2 = {
            'image_type': 1,
            'image_base64': image_base64_encode(image_file)
        }
        images.append(image2)

        op = 'test %s ' % sys._getframe().f_code.co_name
        re = fdb.register(faceset_id=faceset_id, attributes=attributes, images=images)

        self.writelog(re, op)

    def test_fdb_delete(self, fdb):
        faceset_id = '5d3029a7a21c33000804b8e4'
        face_id = '5d3161fcf67f1000085b20f1'

        op = 'test %s ' % sys._getframe().f_code.co_name
        re = fdb.delete(faceset_id,face_id)

        self.writelog(re, op)

    def test_fdb_update_user(self, fdb):
        faceset_id = '5d3029a7a21c33000804b8e4'
        face_id = '5d314db3f67f1000085b20d2'

        attributes = {
            'age': 18,
            'gender': 'male'
        }

        op = 'test %s ' % sys._getframe().f_code.co_name
        re = fdb.update_user(faceset_id, face_id,attributes=attributes)

        self.writelog(re, op)

    def test_fdb_update_user_image(self, fdb):
        faceset_id = '5d3029a7a21c33000804b8e4'
        face_id = '5d314db3f67f1000085b20d2'

        images = []
        image_file = '../../image/wyz_01.jpeg'
        image2 = {
            'image_type': 1,
            'image_base64': image_base64_encode(image_file)
        }
        images.append(image2)
        name = 'update-ttt'
        op = 'test %s ' % sys._getframe().f_code.co_name
        re = fdb.update_user_image(faceset_id, face_id, images)

        self.writelog(re, op)

    def test_fdb_search(self, fdb):
        facesets_id = '5d3029a7a21c33000804b8e4'
        op = 'test %s ' % sys._getframe().f_code.co_name
        re = fdb.search(facesets_id)

        self.writelog(re, op)

    def test_fdb_list(self, fdb):
        faceset_id = '5d3029a7a21c33000804b8e4'
        op = 'test %s ' % sys._getframe().f_code.co_name
        re = fdb.list(faceset_id)

        self.writelog(re, op)


if __name__ == '__main__':
    mac = Auth(ak, sk)
    fdb = faceu.FaceUserManager(mac)

    ht = FaceuTest(log_path='../../log', log_tag='iService',log_file='faceu')
    ht.test_fdb_register(fdb)
    # ht.test_fdb_mkFacesets(fdb=fdb)

    #ht.test_fdb_delete(fdb)
    #ht.test_fdb_update_user(fdb)
    #ht.test_fdb_update_user_image(fdb)
    #ht.test_fdb_list(fdb)
    # ht.test_fdb_search(fdb)
