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
import base64
import json
import logging
import time
from .signalling import WebRTCSignalling, WebRTCSignallingErrorNoPeer
from urllib.parse import quote

import gi
gi.require_version("Gst", "1.0")
gi.require_version('GstWebRTC', '1.0')
gi.require_version('GstSdp', '1.0')
from gi.repository import Gst
from gi.repository import GstWebRTC
from gi.repository import GstSdp

logger = logging.getLogger("webrtc")


class GSTWebRTCAppError(Exception):
    pass


class GSTWebRTCApp:
    def __init__(self,pipeline_str = None,audio = False,audio_str = None):
        """Initialize gstreamer webrtc app.

        Initializes GObjects and checks for required plugins.

        Arguments:
            stun_server {[string]} -- Optional STUN server uri in the form of:
                                    stun:<host>:<port>
            turn_servers {[list of strings]} -- Optional TURN server uris in the form of:
                                    turn://<user>:<password>@<host>:<port>
        """

        self.pipeline = None
        self.webrtcbin = None
        self.data_channel = None

        if not pipeline_str:
            self.pipeline_str  = ''' webrtcbin name=sendrecv bundle-policy=max-bundle
            rpicamsrc name=rpicamsrc bitrate=1000000 preview=false !
            video/x-h264,profile=constrained-baseline,width=640,height=360,level=3.0,framerate=30/1 !
            queue max-size-time=100000000 ! h264parse !
            rtph264pay mtu=1024 config-interval=-1 name=payloader !
            application/x-rtp,media=video,encoding-name=H264,payload=97 ! sendrecv.'''


        if audio and not audio_str:
            self.pipeline_str += ''' alsasrc device=dmic_sv ! audio/x-raw,format=S32LE,rate=48000,channel=2 !
            audioconvert ! audioresample ! queue ! opusenc ! rtpopuspay !
            queue ! application/x-rtp,media=audio,encoding-name=OPUS,payload=96 ! sendrecv.'''
        elif audio and audio_str:
            self.pipeline_str += audio_str



        # WebRTC ICE and SDP events
        self.on_ice = lambda mlineindex, candidate: logger.warn(
            'unhandled ice event')
        self.on_sdp = lambda sdp_type, sdp: logger.warn('unhandled sdp event')

        # Data channel events
        self.on_data_open = lambda: logger.warn('Data channel openned.')
        self.on_data_close = lambda: logger.warn('Data channel closed.')
        self.on_data_error = lambda: logger.warn('Data channel error.')

        Gst.init(None)

        self.check_plugins()

        # Create a new pipeline, elements will be added to this.
        # see build_video_pipeline() and build_audio_pipeline()
        self.pipeline = Gst.Pipeline.new()


    def on_data_message(self,msg):
        """Messages receive by the data channel
        """
        pass

    def send_data_message(self,msg_type,data):
        """Send messages by the data channel
        """
        self.__send_data_channel_message(msg_type,data)


    def check_plugins(self):
        """Check for required gstreamer plugins.

        Raises:
            GSTWebRTCAppError -- thrown if any plugins are missing.
        """

        required = ["opus", "nice", "webrtc", "dtls", "srtp", "rtp", "sctp",
                    "rtpmanager", "ximagesrc"]

        missing = list(
            filter(lambda p: Gst.Registry.get().find_plugin(p) is None, required))
        if missing:
            raise GSTWebRTCAppError('Missing gstreamer plugins:', missing)

    def set_sdp(self, sdp_type, sdp):
        """Sets remote SDP received by peer.

        Arguments:
            sdp_type {string} -- type of sdp, offer or answer
            sdp {object} -- SDP object

        Raises:
            GSTWebRTCAppError -- thrown if SDP is recevied before session has been started.
            GSTWebRTCAppError -- thrown if SDP type is not 'answer', this script initiates the call, not the peer.
        """

        if not self.webrtcbin:
            raise GSTWebRTCAppError('Received SDP before session started')

        if sdp_type != 'answer':
            raise GSTWebRTCAppError('ERROR: sdp type was not "answer"')

        _, sdpmsg = GstSdp.SDPMessage.new()
        GstSdp.sdp_message_parse_buffer(bytes(sdp.encode()), sdpmsg)
        answer = GstWebRTC.WebRTCSessionDescription.new(
            GstWebRTC.WebRTCSDPType.ANSWER, sdpmsg)
        promise = Gst.Promise.new()
        self.webrtcbin.emit('set-remote-description', answer, promise)
        promise.interrupt()

    def set_ice_servers(self,ice_servers):
        for dados in ice_servers:
            urls = dados['urls']
            if 'stun' in urls:
                urls = urls.replace('stun:','stun://')
                self.webrtcbin.set_property("stun-server", urls)
            elif 'turn' in urls:
                turn_address = urls.replace('turn:','').strip()
                turn_cred = dados['credential']
                turn_cred = quote(turn_cred,safe = '')
                turn_username = dados['username']
                turn_username = quote(turn_username,safe = '')
                turn_url = 'turn://{}:{}@{}'.format(turn_username,
                                        turn_cred,
                                        turn_address)
                self.webrtcbin.set_property("turn-server",turn_url)

    def set_ice(self, mlineindex, candidate):
        """Adds ice candidate received from signalling server

        Arguments:
            mlineindex {integer} -- the mlineindex
            candidate {string} -- the candidate

        Raises:
            GSTWebRTCAppError -- thrown if called before session is started.
        """

        logger.info("setting ICE candidate: %d, %s" % (mlineindex, candidate))

        if not self.webrtcbin:
            raise GSTWebRTCAppError('Received ICE before session started')

        self.webrtcbin.emit('add-ice-candidate', mlineindex, candidate)

    def set_video_bitrate(self, bitrate):
        """Set encoder target bitrate in bps

        Arguments:
            bitrate {integer} -- bitrate in bits per second, for example, 2000 for 2kbits/s or 1000000 for 1mbit/sec.
        """

        element = Gst.Bin.get_by_name(self.pipeline, "rpicamsrc")
        element.set_property("bitrate", bitrate)
        self.__send_data_channel_message(
            "pipeline", {"status": "Video bitrate set to: %d" % bitrate})

    def set_framerate(self, framerate):
        """Set encoder target bitrate in bps

        Arguments:
            framerate {integer} -- frames per second
        """

        element = Gst.Bin.get_by_name(self.pipeline, "rpicamsrc")
        element.set_property("framerate", framerate)
        self.__send_data_channel_message(
            "pipeline", {"status": "Video framerate set to: %d" % framerate})

    def is_data_channel_ready(self):
        """Checks to see if the data channel is open.

        Returns:
            [bool] -- true if data channel is open
        """

        return self.data_channel and self.data_channel.get_property("ready-state").value_name == 'GST_WEBRTC_DATA_CHANNEL_STATE_OPEN'

    def __send_data_channel_message(self, msg_type, data):
        """Sends message to the peer through the data channel

        Message is dropped if the channel is not open.

        Arguments:
            msg_type {string} -- the type of message being sent
            data {dict} -- data to send, this is JSON serialized.
        """

        if not self.is_data_channel_ready():
            logger.debug(
                "skipping messaage because data channel is not ready: %s" % msg_type)
            return

        msg = {
            "type": msg_type,
            "data": data,
        }
        self.data_channel.emit("send-string", json.dumps(msg))

    def __on_offer_created(self, promise, _, __):
        """Handles on-offer-created promise resolution

        The offer contains the local description.
        Generate a set-local-description action with the offer.
        Sends the offer to the on_sdp handler.

        Arguments:
            promise {GstPromise} -- the promise
            _ {object} -- unused
            __ {object} -- unused
        """

        promise.wait()
        reply = promise.get_reply()
        offer = reply.get_value('offer')
        promise = Gst.Promise.new()
        self.webrtcbin.emit('set-local-description', offer, promise)
        promise.interrupt()
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.on_sdp('offer', offer.sdp.as_text()))

    def __on_negotiation_needed(self, webrtcbin):
        """Handles on-negotiation-needed signal, generates create-offer action

        Arguments:
            webrtcbin {GstWebRTCBin gobject} -- webrtcbin gobject
        """

        logger.info("handling on-negotiation-needed, creating offer.")
        promise = Gst.Promise.new_with_change_func(
            self.__on_offer_created, webrtcbin, None)
        webrtcbin.emit('create-offer', None, promise)

    def __send_ice(self, webrtcbin, mlineindex, candidate):
        """Handles on-ice-candidate signal, generates on_ice event

        Arguments:
            webrtcbin {GstWebRTCBin gobject} -- webrtcbin gobject
            mlineindex {integer} -- ice candidate mlineindex
            candidate {string} -- ice candidate string
        """

        logger.debug("received ICE candidate: %d %s", mlineindex, candidate)
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.on_ice(mlineindex, candidate))

    def set_gst_null(self):
        self.pipeline.set_state(Gst.State.NULL)
        Gst.init(None)
        self.pipeline = Gst.Pipeline.new()




    def start_pipeline(self,ice_servers):
        """Starts the gstreamer pipeline
        """
        print("Connecting...")
        print("")
        self.pipeline = Gst.parse_launch(self.pipeline_str)
        self.webrtcbin = self.pipeline.get_by_name('sendrecv')
        self.set_ice_servers(ice_servers)

        # Connect signal handlers
        self.webrtcbin.connect(
            'on-negotiation-needed', lambda webrtcbin: self.__on_negotiation_needed(webrtcbin))
        self.webrtcbin.connect('on-ice-candidate', lambda webrtcbin, mlineindex,
                               candidate: self.__send_ice(webrtcbin, mlineindex, candidate))

        # Advance the state of the pipeline to PLAYING.
        res = self.pipeline.set_state(Gst.State.PLAYING)

        if res.value_name != 'GST_STATE_CHANGE_SUCCESS':
            raise GSTWebRTCAppError(
                "Failed to transition pipeline to PLAYING: %s" % res)

        # Create the data channel, this has to be done after the pipeline is PLAYING.
        options = Gst.Structure("application/data-channel")
        # options.set_value("ordered", False)
        # options.set_value("max-retransmits", 0)
        options.set_value("max-packet-lifetime", 100)
        self.data_channel = self.webrtcbin.emit(
            'create-data-channel', "commands", options)

        self.data_channel.connect('on-open', lambda _: self.on_data_open())
        self.data_channel.connect('on-close', lambda _: self.on_data_close())
        self.data_channel.connect('on-error', lambda _: self.on_data_error())
        # self.data_channel.connect(
        #     'on-message-string', lambda _, msg: self.on_data_message(msg))
        self.data_channel.connect(
            'on-message-string', lambda _, msg: asyncio.run(self.on_data_message(msg)))

        logger.warning("pipeline started")
        logger.warning(self.pipeline_str)



class WebRTC:
    def __init__(self,
                device_id,
                ws_server,
                app = None):
        """
        """

        self.device_id = device_id
        self.ws_server = ws_server
        self.app = app
        if not app:
            self.app  = GSTWebRTCApp()

        self.signalling = WebRTCSignalling(
                                            self.app,
                                            self.ws_server,
                                            self.device_id
                                            )
        # Initialize the signalling instance
        self.signalling.on_error = self.on_signalling_error
        # # After connecting, attempt to setup call to peer.
        # self.signalling.on_connect = self.signalling.setup_call
        # Send the local sdp to signalling when offer is generated.
        self.app.on_sdp = self.signalling.send_sdp
        # Send ICE candidates to the signalling server.
        self.app.on_ice = self.signalling.send_ice
        # Set the remote SDP when received from signalling server.
        self.signalling.on_sdp = self.app.set_sdp
        # Set ICE candidates received from signalling server.
        self.signalling.on_ice = self.app.set_ice
        # Start the pipeline once the session is established.
        self.signalling.on_session = self.app.start_pipeline


    # Handle errors from the signalling server.
    async def on_signalling_error(self,e):
        if isinstance(e, WebRTCSignallingErrorNoPeer):
            # Waiting for peer to connect, retry in 2 seconds.
            time.sleep(2)
            await self.signalling.setup_call()
        else:
            logging.error("signalling eror: %s", str(e))

    async def connect(self):
        await self.signalling.connect()

    async def start(self):
        await self.signalling.start()
