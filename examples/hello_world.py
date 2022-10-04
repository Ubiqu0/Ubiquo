import asyncio
import time,logging,json
import sys
import os
sys.path.insert(0, '/home/pi/Ubiquo')

from ubirtc.webrtc import WebRTC,GSTWebRTCApp


WS_SERVER = 'wss://ubiquo.net/ws/control/'
DEVICE_ID = '' #insert your device ID



# define what to do with the received messages
class GstApp(GSTWebRTCApp):
    async def on_data_message(self,msg):
        #message received in the data channel
        msg = json.loads(msg)
        ###########################
        ######## add your code here
        #########################
        if msg['w']['pressed'] is True:
            print("Hello World!")
        ###########################
        ###########################


async def run():

    # #to code directly the pipeline:
    # pipeline_str  = ''' webrtcbin name=sendrecv bundle-policy=max-bundle
    # v4l2src device=/dev/video0 !
    # video/x-h264,profile=constrained-baseline,width=640,height=360,level=3.0,framerate=30/1 !
    # queue max-size-time=100000000 ! h264parse !
    # rtph264pay mtu=1024 config-interval=-1 name=payloader !
    # application/x-rtp,media=video,encoding-name=H264,payload=97 ! sendrecv.'''

    webrct_connection = WebRTC(
                            DEVICE_ID,
                            WS_SERVER,
                            app = GstApp(audio = False,pipeline_str = pipeline_str)
                        )
    await webrct_connection.connect()
    await webrct_connection.start()


if __name__ == "__main__":

    try:
        with open('~/.asoundrc') as f:
            pass
    except Exception as e:
        os.system('cp ~/.asoundrc_bck ~/.asoundrc')

    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run())
        loop.close()
    except Exception as e:
        print("Caught exception: %s" % e)
