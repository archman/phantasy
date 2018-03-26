#!/bin/bash

#
# install
# 

VERSION=1.2.0
cwd=$(pwd)
cd $HOME
git clone -b latest https://github.com/archman/FLAME.git
cd FLAME/deb/trusty
sudo dpkg -i *${VERSION}*.deb
cd ${cwd}

#export PYTHONPATH=/usr/lib/python2.7/dist-packages/:${PYTHONPATH}