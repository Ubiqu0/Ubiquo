import asyncio
import time,logging,json
from ubirtc.webrtc import WebRTC,GSTWebRTCApp

WS_SERVER = 'ws://178.62.245.68:8000/ws/control/'
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
    webrct_connection = WebRTC(
                            DEVICE_ID,
                            WS_SERVER,
                            app = GstApp(audio = False)
                        )
    await webrct_connection.connect()
    await webrct_connection.start()


if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run())
        loop.close()
    except Exception as e:
        print("Caught exception: %s" % e)
