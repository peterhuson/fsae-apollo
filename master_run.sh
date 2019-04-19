
### Display Run Qt App
export ROTATION=90
. setqt5env
screen -S qtscreen /root/fsae-apollo/build/QtE-Demo -qws 

### Run LEDs 
screen -S leds python /root/fsae-apollo/hardware/leds.py

### Run Serial Can Bus adapter
# screen -S canbus 