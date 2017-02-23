#!/bin/bash

# All of the commands to run to install everything on the pi and my general notes until it makes its way into the readme
# Created by Wesley Van Pelt on 2016-12-05

# Just the command to image the SD card on Mac OS so I dont have to keep looking it up
# sudo dd bs=1m if=rasp-lite.img of=/dev/rdiskX

# Default username and password are pi and raspberry
# Changed screen orientation (/boot/config.txt)
# Changed password (passwd)

# Add the file "/etc/systemd/system/getty@tty1.service.d/autologin.conf" for autologin

# Install the required stuff
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install htop mate-core mate-desktop-environment xinit xinput python-tk rhythmbox screenfetch git network-manager-gnome

# Add "startx" to ~/.bash_profile so GUI starts on boot

# Put the startup.sh in ~/ and check the following:
# "xinput --list" Then find input device, in this case it is 'BYZHYYZHY By ZHY851'

# Put in "/etc/NetworkManager/NetworkManager.conf" and "/etc/NetworkManager/NetworkManager.conf"
# Change screensaver settings, wifi/network settings, time, and add startup.sh to the startup stuff in settings
# I had to change timezone settings:
sudo cp /usr/share/zoneinfo/America/Indiana/Indianapolis /etc/localtime

# My cell dongle seemed to just work after going through and using the default settings in network manager and the renaming the device

# Clean up since we're done
sudo apt-get clean


# Navit stuff
sudo apt-get install cmake zlib1g-dev libpng12-dev libgtk2.0-dev librsvg2-bin g++ gpsd gpsd-clients libgps-dev libdbus-glib-1-dev freeglut3-dev libxft-dev libglib2.0-dev libfreeimage-dev gettext
git clone https://github.com/navit-gps/navit.git
