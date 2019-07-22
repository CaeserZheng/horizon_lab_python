#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    : test_pf_visitor_recv.py
@Time    : 2019/7/22 10:47
@Author  : caeser zheng
@Email   : zgl3010@qq.com
"""


from horizon.auth import Auth
from horizon.services.iTools.pf_visitors_recv import GetVisitorByWebsocket
from horizon.example.utils import HorizionTestBase
from horizon.example.test_param_cfg import ak, sk


class VisitorReveTest(HorizionTestBase):

    def test_fdb_visitor_recv_by_ws(self,fdb):
        client_id = 'visitor_sub_space_1'

        fdb.long_conn(client_id=client_id)




if __name__ =='__main__':
    mac = Auth(ak, sk)
    fdb = GetVisitorByWebsocket(mac)

    ht = VisitorReveTest(log_path='../../log', log_tag='iTools',log_file='passengerflow_visitor')
    ht.test_fdb_visitor_recv_by_ws(fdb)

