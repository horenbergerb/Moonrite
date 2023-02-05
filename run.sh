#!/bin/bash

sudo docker run -it \
                -v /tmp/.X11-unix:/tmp/.X11-unix \
                -v $(pwd)/moonrite:/home/moonriteuser/runelite/moonrite \
                -e DISPLAY=$DISPLAY \
                -h $HOSTNAME \
                -v $XAUTHORITY:/home/moonriteuser/.Xauthority \
                moonrite \
                bash
# https://www.osrsbox.com/blog/2019/06/29/building-and-running-runelite-on-the-terminal-using-maven/
# cd runelite-client/target
# java -ea -cp net.runelite.client.Runelite -jar client-1.9.9-SNAPSHOT-shaded.jar --debug --developer-mode