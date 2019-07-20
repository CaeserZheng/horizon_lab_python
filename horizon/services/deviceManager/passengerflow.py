#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    : passengerflow.py
@Time    : 2019/7/18 14:08
@Author  : caeser zheng
@Email   : zgl3010@qq.com
"""

class PassengerFlowManager(object):
    '''
    客流机配置接口，可以用于管理客流机的划线功能，可以用于统计进出店客流以及店外途径客流的等数据
    '''
    def __init__(self, auth):
        self.auth = auth
        self.host = "api-aiot.horizon.ai"
        self.content_type = 'application%2Fjson'

    def pf_line_config(self):
        pass

    def pf_line_search(self):
        pass

    def pf_line_switch(self):
        pass

    def pf_line_delete(self):
        pass


