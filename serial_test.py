import serial as s

serial_port = s.Serial('/dev/ttyAMA1', 9600)
print(serial_port.name)
serial_port.write(b'+++')
ret = serial_port.readline()
print(ret)
