#!/usr/bin/env python
#-.- coding=utf-8 -.-
'''
__author__ = 'caeser'
__mtime__ = '2019/7/18'
'''

from horizon.services.iDevices import recognition
from horizon.auth import Auth
import json,sys
from horizon.example.utils  import HorizionTestBase
from horizon.example.test_param_cfg import ak,sk



class RecognitionTest(HorizionTestBase):

    def test_faceset_build(self,fdb):
        name = '识别机人脸库01'
        op = 'test %s ' % sys._getframe().f_code.co_name
        re = fdb.build(name=name)

        self.writelog(re,op)

    def test_faceset_delete(self,fdb):
        space_id = 'a21c33f35d2d88ad0dac680bdefaultspace'
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
        space_id = 'a21c33f35d2d88ad0dac680b_BQ5KZjor'
        name = 'test_update_space'
        description = 'test update space'
        extra = json.dumps({'enable_analysis_tools':True})

        op = 'test %s ' % sys._getframe().f_code.co_name
        re = fdb.update(space_id=space_id,name=name,description=description,extra=extra)

        self.writelog(re,op)

    def test_space_delete(self, fdb):
        space_id = 'a21c33f35d2d88ad0dac680b_BQ5KZjor'

        op = 'test %s ' % sys._getframe().f_code.co_name
        re = fdb.delete(space_id=space_id)

        self.writelog(re,op)



if __name__ == '__main__':

    mac = Auth(ak,sk)
    fdb = recognition.RecognitionMachineManager(mac)

    ht = RecognitionTest(log_path='../../log',log_tag='iDevice',log_file='recognition')

    #####test space.py
    ht.test_faceset_build(fdb)
    #ht.test_space_build(fdb=fdb)
    #ht.test_space_update(fdb=fdb)
    #ht.test_space_delete(fdb=fdb)
    #ht.test_space_list(fdb=fdb)
    #ht.test_space_space_info(fdb)