# UbiOne


* [Introduction](https://github.com/Ubiqu0/Ubiquo/#introduction)<br>
* [Installation](https://github.com/Ubiqu0/Ubiquo/#installation)<br>



# Introduction

**[Ubiquo](https://ubiquo.net)** is a web application that allows you to live stream and interact with your Raspberry Pi remotely. With **Ubiquo**, one can easily control and interact bots and IoT devices built around and RPI.  Examples are drones or rovers controlled remotely, from miles away,  using a simple web browser.

colocar aqui gif 


# Installation

**Raspberry Pi OS

I have designed **Ubiquo** having in mind its use with a Raspbeery Pi 4. So, the first step is to install [Raspberry Pi OS](https://www.raspberrypi.com/software/operating-systems/) and update it:

```
sudo apt-get update && sudo apt-get upgrade
```

A camera is also expected to be connected to the CSI connector, and the RPI OS configured accordingly: 

1. Go to the RPI system configuration menu by typing ```sudo raspi-config``` in a terminal.
2. Select "**Yes**" to enable the camera.





**Ubiquo** is built on top of [GStreamer](https://gitlab.freedesktop.org/gstreamer) and [WebRTC](https://webrtc.org/), using GStreamer plugin [webrtcbin](https://gstreamer.freedesktop.org/documentation/webrtc/index.html). For this reason, the first step is to install GStreamer and needed plugins. 

Git clone the repository:

```
git clone https://github.com/Ubiqu0/Ubiquo.git
```

cd to the repository and create and enviroment 

