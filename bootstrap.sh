#!/usr/bin/env bash

apt-get update
apt-get install -y vim
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
apt-get install -y python3.6
apt-get install -y python3-pip
export LANG="en_US.UTF-8"
export LC_ALL="en_US.UTF-8"
export LC_CTYPE="en_US.UTF-8"
python3.6 -m pip install cherrypy
python3.6 -m pip install requests 
python3.6 -m pip install numpy 
python3.6 -m pip install scipy 
python3.6 -m pip install control 

