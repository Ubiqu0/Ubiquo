# Ubiquo


* [Introduction](https://github.com/Ubiqu0/Ubiquo/#introduction)<br>
* [Installation](https://github.com/Ubiqu0/Ubiquo/#installation)<br>
  * [RPI OS](https://github.com/Ubiqu0/Ubiquo/#rpi-os)<br>
  * [GStreamer](https://github.com/Ubiqu0/Ubiquo/#gstreamer)<br>
* [Examples](https://github.com/Ubiqu0/Ubiquo/#examples)<br>
* [UbiOne](https://github.com/Ubiqu0/Ubiquo/#ubione)<br>


# Introduction

**[Ubiquo](https://ubiquo.net)** is a web application that allows you to live stream and interact with your Raspberry Pi remotely. With **Ubiquo**, one can easily control and interact bots and IoT devices built around a RPI.  Examples are drones or rovers controlled remotely using a simple web browser.

**Important**: pease note that it is not a professional service but a proof-of-concept demo. It does not offer any warranties, particularly in security.

<p align="center">
  <img src="https://github.com/Ubiqu0/ubiquo_public/blob/main/public/UBIQUO_Control.gif" alt=""/>
</p>


# Installation

## RPI OS

I have designed **Ubiquo** having in mind its use with a Raspbeery Pi 4. Install [Raspberry Pi OS](https://www.raspberrypi.com/software/operating-systems/) (**IMPORTANTE**:don't install Bullseye but the latest stable legacy version of Raspberry Pi OS Buster) and update it:

```
sudo apt-get update && sudo apt-get upgrade
```

A camera is also expected to be connected to the CSI connector, and the RPI OS configured accordingly:

1. Go to the RPI system configuration menu by typing ```sudo raspi-config``` in a terminal.
2. Select "**Interface Options**" > "**Camera**".
3. Select "**Yes**" to enable the camera.

## GStreamer


**Ubiquo** is built on top of [GStreamer](https://gitlab.freedesktop.org/gstreamer) and [WebRTC](https://webrtc.org/), using GStreamer plugin [webrtcbin](https://gstreamer.freedesktop.org/documentation/webrtc/index.html). Start by cloning the repository:


```
git clone https://github.com/Ubiqu0/Ubiquo.git
cd Ubiquo
```

Create and activate a virtual environment:

```
sudo apt-get install virtualenv
virtualenv -p python3 env
source env/bin/activate
```

Then tun the instalattion script:

```
chmod +x install_gstreamer.sh
./install_gstreamer.sh
```

The script will downloand and install GStreamer and several plugins. It will take some time. When finished you can test if GStreamer is installed (note that the first time GStreamer is exectued a bunch of errors will show up):

```
gst-inspect-1.0 --version
```

## ubirtc

Install **ubirtc** python module with:

```
pip install .
```


# Examples

## Ubiquo

The first step is to open an account at [ubiquo.net](http://ubiquo.net/). Log in and create a new device by clicking **"Add new Device"**.

Configuration form:
  * **Name**: device name.
  * **Device ID**: unique device ID.
  * **Resolution**: video resolution.
  * **FPS**: frames per second.
  * **Bitrate**: maximum bitrate at bps.
  * **Send mode**: how data commands are sent to the RPI. Continuously, i.e., commands sent non-stop every "minimum delay" interval, or send and stop when a key is released.

I have configured Ubiquo control room to listen the following keyboard keys:

**q,w,e,r,t,a,s,d,f,g,ArrowRight,ArrowLeft,ArrowDown,ArrowUp**.

Additionally, if connected, the control room reads a **PS4 controller** input.


## Hello World

You have a Hello World example in the [examples](https://github.com/Ubiqu0/Ubiquo/tree/main/examples) folder. Just open it and insert your device ID:

```
WS_SERVER = 'wss://ubiquo.net/ws/control/'
DEVICE_ID = 'XXXXX' #insert your device ID
```

You are now ready to go:

```
python hello_world.py
```

then go to your device control room and click **Connect**. After the connection is established, press the **w** key and check its reception at the RPI terminal.


## Send telemetry

You can send information back to the control room. [send_telemetry.py](https://github.com/Ubiqu0/Ubiquo/blob/main/examples/send_telemetry.py) shows an example of how to do it. It sends a python dictionary every second. The control room is expected to receive a dictionary with a maximum size of eight keys. The keys must be named ```t1,...,t8```, and the values are given by a list in the format ```['Variable name',value]``` or ```['Variable name',value, min, max]```.


## UbiOne

For more complete examples, please check this [repository](https://github.com/Ubiqu0/UbiOne). **UbiOne** is an RPI HAT designed to give remote-ability to an RPI. It joins an STM32F4 MCU, a PCIe connector for 4G (and 5G!) connectivity, and a set of peripherals.


<p align="center">
  <img src="https://user-images.githubusercontent.com/7373193/148281317-fad624ce-be21-4af7-b50f-dae3445dfba5.png" height=475 alt=""/>
</p>
