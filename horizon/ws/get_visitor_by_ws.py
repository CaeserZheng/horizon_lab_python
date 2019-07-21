#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    : get_visitor_by_ws.py
@Time    : 2019/7/21 21:03
@Author  : caeser zheng
@Email   : zgl3010@qq.com
"""

import websocket
import time
from horizon.auth import Auth
try:
    import thread
except ImportError:
    import _thread as thread


class GetVisitorByWebsocket(object):

    def __init__(self,auth):
        self.auth = auth
        self.path = '/ws'
        self.method = 'GET'
        self.host = 'xpushservice-aiot.horizon.ai'
        self.ws_addr = 'ws://{0}{1}'.format(self.host,self.path)

    def on_message(self,ws, message):
        print(message)

    def on_error(self,ws, error):
        print(error)

    def on_close(self,ws):
        print("### closed ###")

    def on_open(self,ws):
        def run(*args):
            for i in range(3):
                time.sleep(1)
                ws.send("Hello %d" % i)
            time.sleep(1)
            ws.close()
            print("thread terminating...")

        thread.start_new_thread(run, ())

    def lisetn(self,client_id):
        headers = {
            'host':self.host,
            'hobot_xpush_client_id':client_id
        }

        authorization = self.auth.get_sign(http_method=self.method,path=self.path,
                                           params=None,headers=headers)
        headers.update({'authorization':authorization})

        h = []
        for k , v in headers.items():
            if not k == 'host':
                h.append('%s:%s' % (k , v))

        #ws_uri = '{0}?authorization={1}'.format(self.ws_addr,authorization)
        ws_uri = '{0}'.format(self.ws_addr)

        print(ws_uri)

        websocket.enableTrace(True)
        ws = websocket.WebSocketApp(ws_uri,
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close,
                                    header=h
                                    )
        #ws.on_open = self.on_open
        ws.run_forever()

if __name__ =='__main__':
    from horizon.test.test_param_cfg import ak , sk

    mac = Auth(ak , sk)
    wst = GetVisitorByWebsocket(mac)

    client_id = 'visitor_sub_space_1'

    wst.lisetn(client_id)