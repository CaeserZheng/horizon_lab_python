#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    : test.py
@Time    : 2019/7/18 14:54
@Author  : caeser zheng
@Email   : zgl3010@qq.com
"""

from horizon.services.intelligentService import facei, facesets, faceu
from horizon.auth import Auth
import unittest
import json
from horizon.record import InfoRecode

ak = 'J1dKGVvbsU7bciqUk0vkC7UB'
sk = 'PrjvA7hWOQojtgt2PYYWkgFXu7bYXnPw'

class HorizionTest(object):

    def __init__(self):
        self.note = InfoRecode()

    def test_fdb_build(self,fdb):
        name = 'office-3'
        discription = 'test office facesets'
        op = 'test facesets build'
        re = fdb.build(name,discription)

        for i in re:
            print(i)
        self.note.add_record(op,re[0])

    def test_fdb_delete(self,fdb):
        facesets_id = '5d303c19f67f1000085b1f27'
        op = 'test facesets build'
        re = fdb.delete(facesets_id)

        for i in re:
            print(i)
        self.note.add_record(op,re[0])




if __name__ == '__main__':

    mac = Auth(ak,sk)
    fdb = facesets.facesetsManager(mac)

    ht = HorizionTest()
    #ht.test_fdb_mkFacesets(fdb=fdb)

    ht.test_fdb_delete(fdb)



