#!/usr/bin/env bash

sudo add-apt-repository ppa:deadsnakes/ppa
apt-get update
apt-get install -y vim
apt-get install -y python3.6
apt-get install -y python3-pip
export LANG="en_US.UTF-8"
export LC_ALL="en_US.UTF-8"
export LC_CTYPE="en_US.UTF-8"
