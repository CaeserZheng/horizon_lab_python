#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    : pf_visitors_recv.py
@Time    : 2019/7/21 21:03
@Author  : caeser zheng
@Email   : zgl3010@qq.com
"""

import websocket
import traceback
import json
import logging
import threading
import time
from horizon.config import _config
from threading import Thread


log = logging.getLogger(__name__)
# logging.basicConfig(level=logging.DEBUG)

class GetVisitorByWebsocket(object):

    def __init__(self,auth,keep_alive=25,num_retries=-1,ws_header=None):
        self.auth = auth
        self.path = '/ws'
        self.method = 'GET'
        self.host = _config['ws_host']
        self.ws_addr = 'ws://{0}{1}'.format(self.host,self.path)

        self.num_retries=num_retries
        self.keep_alive = keep_alive
        self.run_event = threading.Event()

        self.authorization=''
        self.url=''
        self.ws_header =ws_header if ws_header else []

    def short_conn(self,client_id):
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

        websocket.enableTrace(True)
        ws = websocket.create_connection(ws_uri,header=h)
        print(ws.recv())

    def _ping(self):
        # We keep the connection alive by requesting a short object
        while not self.run_event.wait(self.keep_alive):
            log.debug('Sending ping')
            #self.get_objects(["2.8.0"])

    def on_message(self, ws, reply, *args):
        """ This method is called by the websocket connection on every
            message that is received. If we receive a ``notice``, we
            hand over post-processing and signalling of events to
            ``process_notice``.
        """
        log.debug("Received message: %s" % str(reply))
        data = {}
        try:
            data = json.loads(reply, strict=False)
        except ValueError:
            raise ValueError("API node returned invalid format. Expected JSON!")

        print(data)

    def on_close(self, ws):
        """ Called when websocket connection is closed
        """
        log.debug('Closing WebSocket connection with {}'.format(self.ws_addr))

    def on_error(self, ws, error):
        """ Called on websocket errors
        """
        log.exception(error)

    def on_open(self, ws):
        """ This method will be called once the websocket connection is
            established.
        """

        self.keepalive = threading.Thread(
            target=self._ping
        )
        self.keepalive.start()

    def run_forever(self,ws_uri):
        """ This method is used to run the websocket app continuously.
            It will execute callbacks as defined and try to stay
            connected with the provided APIs
        """
        cnt = 0
        while not self.run_event.is_set():
            cnt += 1
            self.url = ws_uri
            log.debug("Trying to connect to node %s" % self.url)
            try:
                websocket.enableTrace(True)
                self.ws = websocket.WebSocketApp(
                    self.url,
                    on_message=self.on_message,
                    on_error=self.on_error,
                    on_close=self.on_close,
                    on_open=self.on_open,
                    header=self.ws_header
                )
                self.ws.run_forever()
            except websocket.WebSocketException as exc:
                print(exc)

                sleeptime = (cnt - 1) * 2 if cnt < 10 else 10
                if sleeptime:
                    log.warning(
                        "Lost connection to node during wsconnect(): %s (%d/%d) "
                        % (self.url, cnt, self.num_retries) +
                        "Retrying in %d seconds" % sleeptime
                    )
                    time.sleep(sleeptime)

            except KeyboardInterrupt:
                self.ws.keep_running = False
                raise

            except Exception as e:
                log.critical("{}\n\n{}".format(str(e), traceback.format_exc()))

    def long_conn(self,client_id):
        headers = {
            'host': self.host,
            'hobot_xpush_client_id': client_id
        }

        authorization = self.auth.get_sign(http_method=self.method, path=self.path,
                                           params=None, headers=headers)
        headers.update({'authorization': authorization})

        for k, v in headers.items():
            if not k == 'host':
                self.ws_header.append('%s:%s' % (k, v))

        # ws_uri = '{0}?authorization={1}'.format(self.ws_addr,authorization)
        ws_uri= '{0}'.format(self.ws_addr)

        self.run_forever(ws_uri=ws_uri)
