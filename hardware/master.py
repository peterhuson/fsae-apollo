import serial as s
from leds import LEDs
 

l = LEDs()
print("got an LED handler!")


serial_port = s.Serial('/dev/ttyAMA3', 9600)
print(serial_port.name)
serial_port.write(b'+++')
ret = serial_port.readline()
print(ret)



