import serial as s
import sys, traceback, os, time
from leds import LEDs
 
class Master:
    def __init__(self):
        self.l = LEDs()
        print("got an LED handler!")

        self.serial_port = s.Serial('/dev/tty.Bluetooth-Incoming-Port', 9600, timeout=1) # Default Serial Baud rate is 9600
        
        self.serial_port = s.Serial('/dev/ttyAMA3', 9600, timeout=1) # Default Serial Baud rate is 9600
        self.serial_port.write(b'+++')
        ret = self.serial_port.readline()
        print(ret)
        self.serial_port.write(b'AT+C=18') # Set CanBus rate to 1Mb/s
        ret = self.serial_port.readline()
        print(ret)
        self.serial_port.write(b'AT+Q')
        ret = self.serial_port.readline()
        print(ret)

        try:
            self.run()
        except KeyboardInterrupt:
            self.shutdown()
        except Exception:
            traceback.print_exc(file=sys.stdout)
            self.shutdown()

    def run(self):
        
        self.fifo_path = '/tmp/myfifo2'

        # FIFO Pipe can only be opened non-blocking when something is reading it
        # try:
        #     os.mkfifo(self.fifo_path)
        # except OSError, e:
        #     print "Failed to create FIFO: %s" % e
        # else:
        #     fifo = open(self.fifo_path, os.O_NONBLOCK)
        #     print("Opened fifo")
        #     fifo.close() 
        #     os.remove(filename)
        #     # pass

        # fifo = open(self.fifo_path, 'w')


        while (True):
            if (self.serial_port.inWaiting()>0): #if incoming bytes are waiting to be read from the serial input buffer
                data_str = self.serial_port.read(self.serial_port.inWaiting())
                print(data_str) 
                
                address = data_str[:4] # Get the first 4 bytes of data
                print(address)

                value = data_str[4:] # Get everything after the first 4 bytes
                print(value)

                if address == 0x118:
                    print("sending {} to leds".format(value))
                    l.displayRPM(value)

                
            time.sleep(0.01)
            print("in read loop")
            #Put the


    def shutdown(self):
        print("Shutdown heard...exiting")
        os.remove(self.fifo_path)


if __name__ == '__main__':
    #try:
    m = Master()
    #except (KeyboardInterrupt, SystemExit):
    # l.shutdown()
    # sys.exit(0)

