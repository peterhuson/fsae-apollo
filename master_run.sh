killall screen

### Display Run Qt App
export ROTATION=90
. setqt5env
screen -dm -S qtscreen /root/fsae-apollo/build/QtE-Demo -qws 

### Run LEDs 
screen -dm -S master_py python /root/fsae-apollo/hardware/master.py

### Run Serial Can Bus adapter
# screen -S canbus 
