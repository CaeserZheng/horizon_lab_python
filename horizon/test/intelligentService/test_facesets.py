#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    : test_facesets.py
@Time    : 2019/7/18 14:54
@Author  : caeser zheng
@Email   : zgl3010@qq.com
"""

from horizon.services.intelligentService import faced, facesets, faceu
from horizon.auth import Auth
import unittest
import json
from horizon.test.utils  import HorizionTestBase
from horizon.test.test_param_cfg import ak,sk


class FacesetsTest(HorizionTestBase):

    def test_fdb_build(self,fdb):
        name = 'office-3'
        discription = 'test office facesets'
        op = 'test facesets build'
        re = fdb.build(name,discription)

        self.writelog(re,op)

    def test_fdb_delete(self,fdb):
        facesets_id = '5d303c19f67f1000085b1f27'
        op = 'test facesets build'
        re = fdb.delete(facesets_id)

        self.writelog(re,op)
    def test_fdb_update(self,fdb):
        facesets_id = '5d3029a7a21c33000804b8e4'
        name = 'update-ttt'
        op = 'test facesets info update'
        re = fdb.update(facesets_id,name=name)

        self.writelog(re, op)

    def test_fdb_search(self,fdb):
        facesets_id = '5d3029a7a21c33000804b8e4'
        op = 'test facesets search by facesets_id'
        re = fdb.search(facesets_id)


        self.writelog(re,op)

    def test_fdb_list(self, fdb):
        op = 'test facesets list'
        re = fdb.list()

        self.writelog(re,op)



if __name__ == '__main__':

    mac = Auth(ak,sk)
    fdb = facesets.facesetsManager(mac)

    ht = FacesetsTest(log_path='../../log',log_tag='intelligentService_facesets')
    #ht.test_fdb_mkFacesets(fdb=fdb)

    #ht.test_fdb_delete(fdb)
    #ht.test_fdb_update(fdb)
    #ht.test_fdb_list(fdb)
    ht.test_fdb_search(fdb)


