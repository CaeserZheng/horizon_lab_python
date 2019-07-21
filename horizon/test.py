#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    : test.py
@Time    : 2019/7/21 18:14
@Author  : caeser zheng
@Email   : zgl3010@qq.com
"""

import time
import horizon.utils as utils

print(utils.ios8601_from_timestamp(int(time.time())))

print(utils.unix_from_datetime('2019-07-06 01:01:01'))