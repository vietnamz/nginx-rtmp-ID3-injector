#!/bin/bash


sudo apt-get update
sudo apt-get install python3 python3-dev python3-pip
sudo apt-get install librtmp-dev
sudo apt-get install libffi-dev
pip3 install -r requirements.txt