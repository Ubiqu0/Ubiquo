#!/bin/bash

sudo apt-get install libx264-dev libjpeg-dev libtool pkg-config  autoconf \
     automake libgstreamer1.0-dev  libgstreamer-plugins-base1.0-dev \
     libgstreamer-plugins-bad1.0-dev gstreamer1.0-plugins-ugly \
     gstreamer1.0-tools gstreamer1.0-gl gstreamer1.0-gtk3 \
     gstreamer1.0-pulseaudio gstreamer1.0-nice \
     libraspberrypi-dev python-gi-dev libgirepository1.0-dev libcairo2-dev \
     virtualenv


git clone https://github.com/thaytan/gst-rpicamsrc.git
cd gst-rpicamsrc
./autogen.sh --prefix=/usr --libdir=/usr/lib/arm-linux-gnueabihf/
make
sudo make install
sudo ldconfig
cd ..

pip install .
