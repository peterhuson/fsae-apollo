## Serial Interface

The Can Bus serial adapter is connected to UART3 through pins 8 and 10. This shows up as `/dev/ttyAMA3` on the NanoPi. The default baud rate is 9600 8N1. Use this wiki to send commands to the Can-Bus device: http://docs.longan-labs.cc/can_bus/

The USBSerial adapter we were using pulls the serial lines higher than normal and therefore doesn't register lows on the bus since they are at around ~2V. See communication with SeeedStudio for more details. 

## LEDs

In order to install the LED package, it is necessary to run the following commands: 
```bash
pip install Adafruit_GPIO
sudo mkdir /usr/lib/python2.7/dist-packages/apa102_led
sudo curl https://raw.githubusercontent.com/tinue/apa102-pi/master/driver/apa102.py -o /usr/lib/python2.7/dist-packages/apa102_led/apa102.py
sudo touch /usr/lib/python2.7/dist-packages/apa102_led/__init__.py
```
