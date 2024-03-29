#!/usr/bin/env python
#-.- coding=utf-8 -.-
'''
__author__ = 'caeser'
__mtime__ = '2019/7/18'
'''

from horizon.services.iDevices import device, pfm_config, space
from horizon.auth import Auth
import json,sys
from horizon.example.utils  import HorizionTestBase
from horizon.example.test_param_cfg import ak,sk



class SpaceTest(HorizionTestBase):

    def test_space_list(self,fdb):
        op = 'test %s ' % sys._getframe().f_code.co_name
        re = fdb.list()

        self.writelog(re,op)

    def test_space_space_info(self,fdb):
        space_id = '6d7c11ff5d7ef2d859f7ad9e_AtlNa0uk'
        op = 'test %s ' % sys._getframe().f_code.co_name
        re = fdb.space_info(space_id)

        self.writelog(re,op)
    def test_space_build(self,fdb):
        name = 'space_build_1'
        description = 'space build 1'
        op = 'test %s ' % sys._getframe().f_code.co_name
        re = fdb.build(name=name,description=description)

        self.writelog(re, op)

    def test_space_update(self,fdb):
        space_id = '6d7c11ff5d7ef2d859f7ad9e_AtlNa0uk'
        name = 'test_update_space'
        description = 'test update space'
        extra = json.dumps({'enable_analysis_tools':True})

        op = 'test %s ' % sys._getframe().f_code.co_name
        re = fdb.update(space_id=space_id,name=name,description=description,extra=extra)

        self.writelog(re,op)

    def test_space_delete(self, fdb):
        space_id = '6d7c11ff5d7ef2d859f7ad9e_AtlNa0uk'

        op = 'test %s ' % sys._getframe().f_code.co_name
        re = fdb.delete(space_id=space_id)

        self.writelog(re,op)



if __name__ == '__main__':

    mac = Auth(ak,sk)
    fdb = space.DeviceSpaceManager(mac)

    ht = SpaceTest(log_path='../../log',log_tag='iDevice',log_file='space')

    #####test space.py
    #ht.test_space_build(fdb=fdb)
    #ht.test_space_update(fdb=fdb)
    #ht.test_space_delete(fdb=fdb)
    ht.test_space_list(fdb=fdb)
    #ht.test_space_space_info(fdb)