#!/bin/bash

# All of the commands to run to install everything on the pi and my general notes until it makes its way into the readme
# Created by Wesley Van Pelt on 2016-12-05
# Last Modified By Wesley Van Pelt on 2016-12-05

# Just the command to image the SD card on Mac OS so I dont have to keep looking it up
# sudo dd bs=1m if=rasp-lite.img of=/dev/rdiskX

# Default username and password are pi and raspberry
# Changed screen orientation (/boot/config.txt)
# Changed password (passwd)

# Add the file "/etc/systemd/system/getty@tty1.service.d/autologin.conf" for autologin

# Install htop, MATE, xinit, xinput, python3, rhythmbox, screenfetch, git, network-manager-gnome
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install htop mate-core mate-desktop-environment xinit xinput python3 rhythmbox screenfetch git network-manager-gnome

# Add "startx" to ~/.bash_profile so GUI starts on boot

# Put the startup.sh in ~/ and check the following:
# "xinput --list" Then find input device, in this case it is 'BYZHYYZHY By ZHY851'

# Put in "/etc/NetworkManager/NetworkManager.conf" and "/etc/NetworkManager/NetworkManager.conf"
# Change screensaver settings, wifi/network settings, time, and add startup.sh to the startup stuff in settings

# Clean up since we're done
sudo apt-get clean
