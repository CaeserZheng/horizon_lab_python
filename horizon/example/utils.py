#!/usr/bin/env python
# -.- coding=utf-8 -.-
'''
__author__ = 'caeser'
__mtime__ = '2019/7/19'
'''

import time
import json
import os
import sys


class InfoRecode(object):
    '''
    记录测试日志
    '''

    def __init__(self, path=None, tag=None, file=None):
        self.recode_log_path = '{0}/{1}'.format(path, tag)
        if not os.path.exists(self.recode_log_path.strip()):
            os.makedirs(self.recode_log_path)
            print('make [%s] success!!' % self.recode_log_path)

        self.recode_log_name = file + '_record.log' if file else 'record.log'

        self.file = '{0}/{1}'.format(self.recode_log_path, self.recode_log_name)

    def add_record(self, op, info):
        re_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
        line = {
            'timestamp': re_time,
            'op': op,
            'info': info
        }
        with open(self.file, 'a+', encoding='utf-8', newline='') as f:
            f.write(json.dumps(line, indent=4) + '\n')


class HorizionTestBase(object):
    '''
    测试类
    '''

    def __init__(self, log_path=None, log_tag=None, log_file=None):
        self.log_path = log_path
        self.log_tag = log_tag
        self.log_file = log_file
        self.note = InfoRecode(log_path, log_tag, log_file)

    def writelog(self, re, op):
        for i in re:
            print(i)
        self.note.add_record(op, re[0]) if re[0] else self.note.add_record(op, re[1].error)
