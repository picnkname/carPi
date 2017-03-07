#!/bin/bash

# All of the commands to run to install everything on the pi and my general notes until it makes its way into the readme
# Created by Wesley Van Pelt on 2016-12-05

# Just the command to image the SD card on Mac OS so I dont have to keep looking it up
# sudo dd bs=1m if=rasp-lite.img of=/dev/rdiskX

# Default username and password are pi and raspberry
# Changed screen orientation (/boot/config.txt)

# apt update
# apt upgrade
# apt install git
cd /home/pi
git clone https://github.com/wesley5040/carPi.git
cp /home/pi/carPi/configsAndScripts/.bash_profile /home/pi/.bash_profile
cp /home/pi/carPi/configsAndScripts/startup.sh /home/pi/startup.sh
sudo su
cp /home/pi/carPi/configsAndScripts/config.txt /boot/config.txt
cp /home/pi/carPi/configsAndScripts/autologin.conf /etc/systemd/system/getty@tty1.service.d/autologin.conf

# Install the required stuff
apt install htop mate-core mate-desktop-environment xserver-xorg xinit xinput python-tk screenfetch network-manager-gnome gpsd gpsd-clients python-gps python3 vlc pavucontrol

# Check the following in ~/startup.sh:
# "xinput --list" Then find input device, in this case it is 'BYZHYYZHY By ZHY851'

# Put in "/etc/NetworkManager/NetworkManager.conf" and "/etc/NetworkManager/NetworkManager.conf"
# Change screensaver settings, wifi/network settings, time, and add startup.sh to the startup stuff in settings
# Change sound output
# I had to change timezone settings:
cp /usr/share/zoneinfo/America/Indiana/Indianapolis /etc/localtime


# Navit stuff
apt install cmake zlib1g-dev libpng12-dev libgtk2.0-dev librsvg2-bin g++ gpsd gpsd-clients libgps-dev libdbus-glib-1-dev freeglut3-dev libxft-dev libglib2.0-dev libfreeimage-dev gettext
git clone https://github.com/navit-gps/navit.git
