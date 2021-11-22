import asyncio
import time,logging,json
from ubirtc.webrtc import WebRTC,GSTWebRTCApp
import serial

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
        pressed = []
        if msg['q']['pressed'] is True:
            pressed.append('q')
        if msg['w']['pressed'] is True:
            pressed.append('w')
        if msg['e']['pressed'] is True:
            pressed.append('e')
        if msg['r']['pressed'] is True:
            pressed.append('r')

        if pressed:
            print("Pressed:",','.join(pressed))
        ###########################
        ###########################


async def send_data_message(wrtc_conn):
    count = 0
    while True:
        await asyncio.sleep(1)
        if wrtc_conn.is_data_channel_ready():
            ###########################
            ######## add your code here
            #########################
            # send dictionary with t1,t2,...,t8 as keys and the respective value with the format ['name',value]
            # If you want a progressive you can send the min and max with ['name',value,min,max]
            data = {
                't1':['Var1',count],
                't2':['Var2',count*2,0,100],
                }
            count+=1
            ###########################
            ###########################


            wrtc_conn.send_data_message('telemetry',data)


async def run():
    webrct_connection = WebRTC(
                            DEVICE_ID,
                            WS_SERVER,
                            app = GstApp(audio = False)
                        )
    asyncio.ensure_future(send_data_message(webrct_connection.app))
    await webrct_connection.connect()
    await webrct_connection.start()


if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run())
        loop.close()
    except Exception as e:
        print("Caught exception: %s" % e)
