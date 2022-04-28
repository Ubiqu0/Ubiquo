#!/bin/bash


VERSION=1.20.1
ENVPATH=/home/pi/Ubiquo/env

mkdir gstreamer-$VERSION
cd gstreamer-$VERSION

wget wget https://gitlab.freedesktop.org/libnice/libnice/-/archive/0.1.18/libnice-0.1.18.tar
wget https://gstreamer.freedesktop.org/src/gstreamer/gstreamer-$VERSION.tar.xz
wget https://gstreamer.freedesktop.org/src/gst-plugins-base/gst-plugins-base-$VERSION.tar.xz
wget https://gstreamer.freedesktop.org/src/gst-plugins-good/gst-plugins-good-$VERSION.tar.xz
wget https://gstreamer.freedesktop.org/src/gst-plugins-bad/gst-plugins-bad-$VERSION.tar.xz
wget https://gstreamer.freedesktop.org/src/gst-python/gst-python-$VERSION.tar.xz
for a in `ls -1 *.tar*`; do tar -xf $a; done

sudo apt-get install build-essential cmake meson flex bison \
      libglib2.0-dev mesa-utils libgtk2.0-dev libx264-dev libx264-dev \
      python-gi-dev libgirepository1.0-dev libcairo2-dev python3-gst-1.0 autoconf \
      libopus-dev gtk-doc-tools libtool libsrtp2-dev openssl libssl-dev \
      alsa-utils alsa-utils libalsa-ocaml  libasound2-dev libatlas-base-dev \
      libjson-glib-dev libegl-dev libvpx-dev -y

pip3 install meson pycairo PyGObject smbus2 websockets pyserial

cd gstreamer-$VERSION
mkdir build && cd build
meson  --prefix=/usr       \
       --buildtype=release \
       -Dgst_debug=false   \
       -Dpackage-origin=https://www.linuxfromscratch.org/blfs/view/svn/ \
       -Dpackage-name="GStreamer 1.20.1 BLFS" &&
ninja && sudo ninja install && sudo ldconfig
cd ../../

cd gst-plugins-base-$VERSION
mkdir build && cd build
meson  --prefix=/usr       \
       --buildtype=release \
       -Dgl=disabled \
       -Dpackage-origin=https://www.linuxfromscratch.org/blfs/view/svn/ \
       -Dpackage-name="GStreamer 1.20.1 BLFS"    \
       --wrap-mode=nodownload &&
ninja && sudo ninja install && sudo ldconfig
cd ../../

cd libnice-0.1.18
mkdir build && cd build
meson --prefix=/usr
ninja && sudo ninja install && sudo ldconfig
cd ../../


cd gst-plugins-good-$VERSION
mkdir build && cd build
meson  --prefix=/usr       \
       --buildtype=release \
       -Dpackage-origin=https://www.linuxfromscratch.org/blfs/view/svn/ \
       -Dpackage-name="GStreamer 1.20.1 BLFS"
ninja && sudo ninja install && sudo ldconfig
cd ../../


cd gst-plugins-bad-$VERSION
mkdir build && cd build
meson  --prefix=/usr       \
       --buildtype=release \
       -Dpackage-origin=https://www.linuxfromscratch.org/blfs/view/svn/ \
       -Dpackage-name="GStreamer 1.20.1 BLFS"
ninja && sudo ninja install && sudo ldconfig
cd ../../

cd gst-python-$VERSION
mkdir build && cd build
meson --prefix=$ENVPATH -Dbuildtype=release -Dlibpython-dir=/usr/lib/arm-linux-gnueabihf ..
ninja && sudo ninja install &&  sudo ldconfig
cd ../../
