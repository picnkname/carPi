#/bin/bash

# Fix touchsceen stuff
xinput set-prop 'BYZHYYZHY By ZH851' 'Evdev Axes Swap' 1
xinput --set-prop 'BYZHYYZHY By ZH851' 'Evdev Axis Inversion' 0 1 # may need to swap last 2 ints

# Start carPi GUI
cd ~/carPi/pythonApp
python app.py

