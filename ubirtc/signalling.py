# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#Modifications copyright (C) 2021 Miguel Won


import asyncio
import json
import logging
import time
import websockets

import gi
gi.require_version("Gst", "1.0")
gi.require_version('GstWebRTC', '1.0')
gi.require_version('GstSdp', '1.0')
from gi.repository import Gst
from gi.repository import GstWebRTC
from gi.repository import GstSdp


logger = logging.getLogger("signalling")

"""Signalling API for Gstreamer WebRTC demo

"""

class WebRTCSignallingError(Exception):
    pass

class WebRTCSignallingErrorNoPeer(Exception):
    pass

class WebRTCSignalling:
    def __init__(self, app,ws_server,device_id):
        """Initialize the signalling instnance

        """
        self.app = app
        self.ws_server = ws_server
        self.device_id = device_id
        self.conn = None
        self.started = 0

        self.on_ice = lambda mlineindex, candidate: logger.warn(
            'unhandled ice event')
        self.on_sdp = lambda sdp_type, sdp: logger.warn('unhandled sdp event')
        self.on_connect = lambda: logger.warn('unhandled on_connect callback')
        self.on_session = lambda: logger.warn('unhandled on_session callback')
        self.on_error = lambda v: logger.warn(
            'unhandled on_error callback: %s', v)

    async def connect(self):
        """Connects to and registers id with signalling server
        """
        uri = self.ws_server + self.device_id + '/'
        self.conn = await websockets.connect(uri)
        logger.warning(f"DEVICE ID:{self.device_id}")
        await self.conn.send(json.dumps({'message':'device_on','type':'system','user':'device'}))

    async def send_ice(self, mlineindex, candidate):
        """Sends te ice candidate to peer

        Arguments:
            mlineindex {integer} -- the mlineindex
            candidate {string} -- the candidate
        """
        msg = {'ice': {'candidate': candidate, 'sdpMLineIndex': mlineindex}}
        msg = {'type':'signalling','message':msg,'user':'device'}
        msg = json.dumps(msg)
        logger.debug(f"Send ICE candidate: {msg}")
        await self.conn.send(msg)

    async def send_sdp(self, sdp_type, sdp):
        """Sends the SDP to peer

        Arguments:
            sdp_type {string} -- SDP type, answer or offer.
            sdp {string} -- the SDP
        """

        logger.info("sending sdp type: %s" % sdp_type)
        logger.debug("SDP:\n%s" % sdp)

        msg = {'sdp': {'type': sdp_type, 'sdp': sdp}}
        msg = {'type':'signalling','message':msg,'user':'device'}
        msg = json.dumps(msg)

        await self.conn.send(msg)

    async def start(self):
        """Handles messages from the signalling server websocket.
        """
        async for message in self.conn:
            data = json.loads(message)
            msg_type = data['type']
            user = data['user']
            msg = data['message']
            if user == 'device':
                continue

            if msg_type == 'signalling' and user == 'browser' and 'ice_servers' in msg:
                self.ice_servers = msg['ice_servers']

            if msg == 'browser_on':
                await self.conn.send(json.dumps({'type':'system','message':'device_on','user':'device'}))

            if msg == 'left_room':
                self.app.set_gst_null()
                self.started = 0

            if msg_type == 'command':
                if not self.started and msg['action'] == 'start' and self.ice_servers:
                    fps = msg['fps']
                    bitrate = msg['bitrate']
                    resolution = msg['resolution'].split('x')
                    logger.warning(f"FPS:{fps} | Bitrate:{bitrate} | Resolution:{resolution}")
                    self.app.pipeline_str = self.app.pipeline_str.replace('bitrate=1000000','bitrate={}000'.format(bitrate))
                    self.app.pipeline_str = self.app.pipeline_str.replace('framerate=30','framerate={}'.format(fps))
                    self.app.pipeline_str = self.app.pipeline_str.replace('width=640,height=360','width={},height={}'.format(resolution[0],resolution[1]))
                    self.app.start_pipeline(self.ice_servers)
                    self.started = 1
                if msg['action'] == 'close':
                    self.app.set_gst_null()
                    self.started = 0


            elif 'ice' in msg:
                logger.info("received ICE")
                logger.debug("ICE:\n%s" % msg.get("ice"))
                self.on_ice(msg['ice'].get('sdpMLineIndex'),
                           msg['ice'].get('candidate'))
            elif 'sdp' in msg:
                logger.info("received SDP")
                logger.debug("SDP:\n%s" % msg["sdp"])
                self.on_sdp(msg['sdp'].get('type'),
                            msg['sdp'].get('sdp'))
