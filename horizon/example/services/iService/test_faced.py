#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    : test_facesets.py
@Time    : 2019/7/18 14:54
@Author  : caeser zheng
@Email   : zgl3010@qq.com
"""

from horizon.services.iServices import faced, facesets, faceu
from horizon.auth import Auth
import unittest
import json
from horizon.example.utils import HorizionTestBase
from horizon.example.test_param_cfg import ak, sk
from horizon.utils import image_base64_encode, image_base64_decode
import time


class FacedTest(HorizionTestBase):

    def test_fdb_detect(self, fdb):
        image_type = 0

        single_people = 'http://z-qn-oss.ultrakevin.top/horizon_faseu/person_career.jpg'
        mult_people = 'https://z-qn-oss.ultrakevin.top/horizion/faced_test/allstart.jpg'
        image_url = mult_people

        image_file = ''
        image_obj = image_url

        max_face_count = 100
        keypoint = True
        quality = True

        attributes = ['pose', 'age', 'gender', 'feature']
        attr = ','.join(attributes)

        op = 'test faced detet'
        re = fdb.detect(image_type=image_type, image_obj=image_obj, attributes=attr,
                        max_face_count=max_face_count, keypoint=keypoint, quality=quality)

        self.writelog(re, op)

        face_num = len(re[0]['data']['face_info'])
        print('识别人脸个数：%d' % face_num)



    def test_fdb_face_match(self, fdb):
        image_type = 0

        pic1 = 'https://z-qn-oss.ultrakevin.top/horizion/faced_test/james.png'
        pic2 = 'https://z-qn-oss.ultrakevin.top/horizion/faced_test/james2.jpg'
        image_url_1 = pic1
        image_url_2 = pic2

        image_obj_1 = image_url_1
        image_obj_2 = image_url_2
        op = 'test faced match'
        re = fdb.match(image_type=image_type, image_obj_1=image_obj_1,image_obj_2=image_obj_2)

        self.writelog(re, op)

    def test_fdb_face_search(self, fdb):
        image_type = 0

        pic = 'http://z-qn-oss.ultrakevin.top/horizon_faseu/person_career.jpg'
        image_url = pic

        image_file = ''
        image_obj = image_url

        faceset_id = '5d3029a7a21c33000804b8e4'
        faceset_ids = [faceset_id]

        op = 'test faced search'
        re = fdb.search(image_type=image_type, image_obj=image_obj, faceset_ids=faceset_ids)

        self.writelog(re, op)

    def test_fdb_face_extract(self, fdb):
        image_type = 0

        single_people = 'http://z-qn-oss.ultrakevin.top/horizon_faseu/person_career.jpg'
        #mult_people = 'https://z-qn-oss.ultrakevin.top/horizion/faced_test/wujiandao.jpg'
        mult_people = 'https://z-qn-oss.ultrakevin.top/horizion/faced_test/allstart.jpg'
        image_url = mult_people

        image_file = ''
        image_obj = image_url

        max_face_count = 100

        op = 'test faced extract'
        re = fdb.face_extract(image_type=image_type, image_obj=image_obj, max_face_count=max_face_count)

        count = 0
        request_id = re[0]['request_id']
        for i in re[0]['data']:
            count += 1
            image_file = '{0}/image/{1}_{2}_{3}.jpg'.format(self.log_path,request_id,int(time.time()),count)
            print(image_base64_decode(image_file,i['image_base64']))

        self.writelog(re, op)


if __name__ == '__main__':
    mac = Auth(ak, sk)
    fdb = faced.FaceDetect(mac)

    ht = FacedTest(log_path='../../log', log_tag='iService',log_file='faced')
    #ht.test_fdb_detect(fdb)
    ht.test_fdb_face_extract(fdb)
    #ht.test_fdb_face_search(fdb)
    #ht.test_fdb_face_match(fdb)
