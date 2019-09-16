#!/usr/bin/env bash

apt-get update
apt-get install -y vim
apt-get install -y python3
apt-get install -y python3-pip
pip3 install cherrypy
pip3 install requests
export LANG="en_US.UTF-8"
export LC_ALL="en_US.UTF-8"
export LC_CTYPE="en_US.UTF-8"
pip3 install numpy
