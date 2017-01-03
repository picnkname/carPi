#/bin/bash

# Fix touchsceen stuff
xinput set-prop 'BYZHYYZHY By ZH851' 'Evdev Axes Swap' 1
xinput --set-prop 'BYZHYYZHY By ZH851' 'Evdev Axis Inversion' 0 1 # may need to swap last 2 ints

# Start carPi GUI (app.py will launch Rhythmbox)
cd ~/carPi/pythonApp
python app.py

# nm-applet crashes on startup for some reason, so restart it after a bit
sleep 5
nm-applet

