#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    : record.py
@Time    : 2019/7/18 16:30
@Author  : caeser zheng
@Email   : zgl3010@qq.com
"""
import json
import time


class InfoRecode(object):
    def __init__(self,file=None):
        defind_file = 'record.log'
        self.file = file if file else defind_file

    def add_record(self, op,info):
        re_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        line = {
            'timestamp':re_time,
            'op':op,
            'info':info
        }
        with open(self.file, 'a+', encoding='utf-8', newline='') as f:
            #print(json.dumps(line))
            f.write(json.dumps(line,indent=4) + '\n')

'''
if __name__ == '__main__':
    path = 'test.db'
    ifr = InfoRecode(path)

    op = 'test'
    info = {
        'name': 'zheng1',
        'id': 2
    }
    ifr.add_record(op,info)
'''