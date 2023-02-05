#!/bin/bash

# https://stackoverflow.com/questions/44429394/x11-forwarding-of-a-gui-app-running-in-docker
xhost +local:docker

sudo docker build -t moonrite . | tee moonrite/logs/dockerbuild.log