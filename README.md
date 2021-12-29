# UbiOne


* [Introduction](https://github.com/Ubiqu0/Ubiquo/#introduction)<br>
* [Installation](https://github.com/Ubiqu0/Ubiquo/#installation)<br>
* [RPI OS](https://github.com/Ubiqu0/UbiOne/#rpi-os)<br>
* [GStreamer](https://github.com/Ubiqu0/UbiOne/#gstreamer)<br>



# Introduction

**[Ubiquo](https://ubiquo.net)** is a web application that allows you to live stream and interact with your Raspberry Pi remotely. With **Ubiquo**, one can easily control and interact bots and IoT devices built around a RPI.  Examples are drones or rovers controlled remotely using a simple web browser.

colocar aqui gif 


# Installation

## RPI OS

I have designed **Ubiquo** having in mind its use with a Raspbeery Pi 4. So, the first step is to install [Raspberry Pi OS](https://www.raspberrypi.com/software/operating-systems/) and update it:

```
sudo apt-get update && sudo apt-get upgrade
```

A camera is also expected to be connected to the CSI connector, and the RPI OS configured accordingly: 

1. Go to the RPI system configuration menu by typing ```sudo raspi-config``` in a terminal.
2. Select "**Yes**" to enable the camera.

## GStreamer


**Ubiquo** is built on top of [GStreamer](https://gitlab.freedesktop.org/gstreamer) and [WebRTC](https://webrtc.org/), using GStreamer plugin [webrtcbin](https://gstreamer.freedesktop.org/documentation/webrtc/index.html). For this reason, the first step is to install GStreamer and needed plugins. 

Git clone the repository and run the script ``install_gstreamer.sh``:

```
git clone https://github.com/Ubiqu0/Ubiquo.git
cd Ubiquo
```

Before run the instalattion scrip you must create and activate a virtual environment:

```
sudo apt-get install virtualenv
virtualenv -p python3 env
source env/bin/activate
```

Run the instalattion script:

```
chmod +x install_gstreamer.sh
./install_gstreamer.sh
```

The script will downloand and install GStreamer and several plugins, so it will take some time. When finished you can test if GStreamer is installed with (note that the first GStreamer is exectued a bunch of errors will show up):

```
gst-inspect-1.0 --version
```

Finnaly, you can install **ubirtc** python module with:

```
pip install .
```






