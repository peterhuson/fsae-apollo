import socket
import sys

#We assume that a socket 

#Create 
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

#Connect
server_address = './comms_socket'
printf('connecting to {}'.format(server_address))
try:
    sock.connect(server_address)
except: socket.error as msg:
    printf(msg)
    sys.exit(1)

try:

    #Send data
    message = 'Hello Socket!'
    sock.sendall(message)
    #Assume we get 'ack' back
    msg = 'ack'
    data_recv = 0
    data_size = len(msg)

    while data_recv < data_size:
        data = sock.recv(16)
        data_recv += len(data)
        print('{!r}'.format(data))
    


finally:
    print('exiting socket')
    sock.close()
