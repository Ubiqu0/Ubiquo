#!/bin/bash

VERSION=1.18.4
ENVPATH=/home/pi/Ubiquo/env

mkdir gstreamer_$VERSION
cd gstreamer_$VERSION

wget https://gstreamer.freedesktop.org/src/gst-plugins-base/gst-plugins-base-$VERSION.tar.xz
wget https://gstreamer.freedesktop.org/src/gstreamer/gstreamer-$VERSION.tar.xz
wget https://gstreamer.freedesktop.org/src/gst-plugins-ugly/gst-plugins-ugly-$VERSION.tar.xz
wget https://gstreamer.freedesktop.org/src/gst-plugins-good/gst-plugins-good-$VERSION.tar.xz
wget https://gstreamer.freedesktop.org/src/gst-plugins-bad/gst-plugins-bad-$VERSION.tar.xz
wget https://gstreamer.freedesktop.org/src/gst-omx/gst-omx-$VERSION.tar.xz
wget https://gstreamer.freedesktop.org/src/gst-python/gst-python-$VERSION.tar.xz
for a in `ls -1 *.tar.*`; do tar -xf $a; done

sudo apt-get install build-essential cmake meson flex bison \
      libglib2.0-dev mesa-utils libgtk2.0-dev libnice-dev libx264-dev libx264-dev \
      python-gi-dev libgirepository1.0-dev libcairo2-dev python3-gst-1.0 autoconf \
      libopus-dev gtk-doc-tools libtool libsrtp2-dev openssl libssl-dev \
      alsa-utils alsa-utils libalsa-ocaml  libasound2-dev python-dev libatlas-base-dev libjson-glib-dev -y



pip install pycairo PyGObject smbus2 websockets pyserial


cd gstreamer-$VERSION
mkdir build && cd build
meson --prefix=/usr       \
        --wrap-mode=nofallback \
        -D buildtype=release \
        -D gst_debug=false ..
ninja -j4 && sudo ninja install && sudo ldconfig
cd ../../


cd gst-plugins-base-$VERSION
mkdir build && cd build
meson --prefix=/usr -D buildtype=release ..
ninja -j4 && sudo ninja install && sudo ldconfig
cd ../../

cd gst-plugins-good-$VERSION
mkdir build && cd build
meson --prefix=/usr -D buildtype=release ..
ninja -j4 && sudo ninja install && sudo ldconfig
cd ../../

git clone https://gitlab.freedesktop.org/libnice/libnice.git
cd libnice
mkdir build && cd build
meson --prefix=/usr -D buildtype=release ..
ninja -j4 && sudo ninja install && sudo ldconfig
cd ../../


cd gst-plugins-ugly-$VERSION
mkdir build && cd build
meson --prefix=/usr -D buildtype=release ..
ninja -j4 && sudo ninja install && sudo ldconfig
cd ../../

cd gst-plugins-bad-$VERSION
mkdir build && cd build
meson --prefix=/usr -D buildtype=release ..
ninja -j4 && sudo ninja install && sudo ldconfig
cd ../../

cd gst-omx-$VERSION
mkdir build && cd build
meson --prefix=/usr -D target=rpi -D header_path=/opt/vc/include/IL
ninja -j4 && sudo ninja install && sudo ldconfig
cd ../../

cd gst-python-$VERSION
mkdir build && cd build
meson --prefix=$ENVPATH -D buildtype=release -D gst_debug=false -D gtk_doc=disabled -D libpython-dir=/usr/lib/arm-linux-gnueabihf ..
ninja -j4 && sudo ninja install &&  sudo ldconfig
cd ../../
