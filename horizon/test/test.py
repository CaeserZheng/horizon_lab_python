#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    : test.py
@Time    : 2019/7/19 11:24
@Author  : caeser zheng
@Email   : zgl3010@qq.com
"""
import horizon.utils as us


if __name__ == '__main__':
    file = 'E:\个人\职业.JPG'
    print(us.image_base64_encode(file))