FROM ubuntu:latest

#https://stackoverflow.com/questions/64252361/tkinter-install-in-docker
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=US

# https://stackoverflow.com/questions/27701930/how-to-add-users-to-docker-container
RUN groupadd -g 1000 moonriteuser
RUN useradd -rm -d /home/moonriteuser -s /bin/bash -g 1000 -u 1000 moonriteuser
RUN adduser moonriteuser sudo

RUN apt-get -y update
RUN apt-get -y install openjdk-11-jdk
RUN apt-get -y install maven
RUN apt-get -y install git
RUN apt-get -y install python3-tk
RUN apt-get -y install python3-dev
RUN apt-get -y install python3-pip
RUN apt-get -y install scrot

RUN pip install --upgrade pip
RUN pip install numpy pyautogui torch opencv-python pyyaml pandas pynput Pillow

USER moonriteuser
WORKDIR /home/moonriteuser

RUN git clone https://github.com/runelite/runelite.git
# https://www.osrsbox.com/blog/2019/06/29/building-and-running-runelite-on-the-terminal-using-maven/
WORKDIR "/home/moonriteuser/runelite"
RUN mvn install -DskipTests

WORKDIR "/home/moonriteuser/runelite/moonrite"