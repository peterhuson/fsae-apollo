import serial as s
from leds import LEDs
 
l = LEDs()
print("got an LED handler!")

serial_port = s.Serial('/dev/ttyAMA3', 9600, timeout=1)
print(serial_port.name)
serial_port.write(b'+++')
ret = serial_port.readline()
print(ret)
serial_port.write(b'AT+C=18')
ret = serial_port.readline()
print(ret)
serial_port.write(b'+++')
ret = serial_port.readline()
print(ret)

while (True):
    # NB: for PySerial v3.0 or later, use property `in_waiting` instead of function `inWaiting()` below!
    if (serial_port.inWaiting()>0): #if incoming bytes are waiting to be read from the serial input buffer
        data_str = serial_port.read(serial_port.inWaiting()).decode('ascii') #read the bytes and convert from binary array to ASCII
        print(data_str, end='') #print the incoming string without putting a new-line ('\n') automatically after every print()
    #Put the


