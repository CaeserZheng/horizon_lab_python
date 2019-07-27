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
import json,sys
from horizon.example.utils  import HorizionTestBase
from horizon.example.test_param_cfg import ak,sk


class FacesetsTest(HorizionTestBase):

    def test_fdb_build(self,fdb):
        name = 'office-3'
        discription = 'test office facesets'

        op = 'test %s ' % sys._getframe().f_code.co_name
        re = fdb.build(name,discription=discription)

        self.writelog(re,op)

    def test_fdb_delete(self,fdb):
        facesets_id = '5d303c19f67f1000085b1f27'
        op = 'test facesets build'
        re = fdb.delete(facesets_id)

        self.writelog(re,op)
    def test_fdb_update(self,fdb):
        facesets_id = '5d3029a7a21c33000804b8e4'
        name = 'update-ttt'
        op = 'test %s ' % sys._getframe().f_code.co_name
        re = fdb.update(facesets_id,name=name)

        self.writelog(re, op)

    def test_fdb_search(self,fdb):
        facesets_id = '5d3029a7a21c33000804b8e4'
        op = 'test %s ' % sys._getframe().f_code.co_name
        re = fdb.search(facesets_id)


        self.writelog(re,op)

    def test_fdb_list(self, fdb):
        op = 'test %s ' % sys._getframe().f_code.co_name
        re = fdb.list()

        self.writelog(re,op)



if __name__ == '__main__':

    mac = Auth(ak,sk)
    fdb = facesets.FaceSetsManager(mac)

    ht = FacesetsTest(log_path='../../log',log_tag='iService',log_file='facesets')
    ht.test_fdb_build(fdb)

    #ht.test_fdb_delete(fdb)
    #ht.test_fdb_update(fdb)
    #ht.test_fdb_list(fdb)
    #ht.test_fdb_search(fdb)



