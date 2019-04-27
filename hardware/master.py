import serial as s
from leds import LEDs
 
class Master:
    def __init__(self):
        self.l = LEDs()
        print("got an LED handler!")

        serial_port = s.Serial('/dev/ttyAMA3', 9600, timeout=1) # Default Serial Baud rate is 9600
        print(serial_port.name)
        serial_port.write(b'+++')
        ret = serial_port.readline()
        print(ret)
        serial_port.write(b'AT+C=18') # Set CanBus rate to 1Mb/s
        ret = serial_port.readline()
        print(ret)
        serial_port.write(b'AT+Q')
        ret = serial_port.readline()
        print(ret)

        try:
            self.run()
        except KeyboardInterrupt:
            print "Shutdown requested...exiting"
            self.shutdown()
        except Exception:
            traceback.print_exc(file=sys.stdout)
        sys.exit(0)

    def run(self):
        

        fifo_path = '/tmp/myfifo2'
        os.mkfifo(fifo_path)
        fifo_write = open(fifo_path, 'w')
        fifo_write.close()

        # while (True):
        #     # NB: for PySerial v3.0 or later, use property `in_waiting` instead of function `inWaiting()` below!
        #     if (serial_port.inWaiting()>0): #if incoming bytes are waiting to be read from the serial input buffer
        #         data_str = serial_port.read(serial_port.inWaiting()).decode('ascii') #read the bytes and convert from binary array to ASCII
        #         print(data_str) #print the incoming string without putting a new-line ('\n') automatically after every print()
                
        #     time.sleep(0.01)
            #Put the


    def shutdown(self):
        os.remove(fifo_path)


if __name__ == '__main__':
    #try:
    m = Master()
    #except (KeyboardInterrupt, SystemExit):
    # l.shutdown()
    # sys.exit(0)

