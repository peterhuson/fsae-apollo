import serial as s
import sys, traceback, os, time
from leds import LEDs
 
class Master:
    def __init__(self):
        self.l = LEDs()
        self.l.displayRPM(9500)
        print("got an LED handler!")

        # self.serial_port = s.Serial('/dev/tty.Bluetooth-Incoming-Port', 9600, timeout=1) # Default Serial Baud rate is 9600
        
        # self.serial_port = s.Serial('/dev/ttyAMA3', 9600, timeout=1) # Default Serial Baud rate is 9600
        # self.serial_port.write(b'+++')
        # ret = self.serial_port.readline()
        # print(ret)
        # # self.serial_port.write(b'AT+C=18\n') # Set CanBus rate to 1Mb/s
        # self.serial_port.write(b'AT+C=13\n') # Set CanBus rate to 125Kb/s
        # ret = self.serial_port.readline()
        # print(ret)
        # self.serial_port.write(b'AT+Q\n')
        # ret = self.serial_port.readline()
        # print(ret)
        # time.sleep(0.1)

        try:
            self.run()
        except KeyboardInterrupt:
            self.shutdown()
        except Exception:
            traceback.print_exc(file=sys.stdout)
            self.shutdown()

    def run(self):
        
        self.fifo_path = '/tmp/myfifo2'

        try:
            os.mkfifo(self.fifo_path, 644)
            print("Made Fifo")
        except OSError, e:
            print "Failed to create FIFO: %s" % e
        
        print("Waiting on fifo pipe")
        # This will block until the reading side is open
        self.fifo = os.open(self.fifo_path, os.O_WRONLY)
        print("Opened fifo")
        os.write(self.fifo, "Beginning Pipe Messages\n") 
            # pass

        # fifo = open(self.fifo_path, 'w')

        self.serial_port = s.Serial('/dev/ttyAMA3', 115200, timeout=1) # Serial Baud rate from Arduino is 115200
        print("Got serial from Arduino")
        

        os.write(self.fifo, "ctmp:100.0\n")
        os.write(self.fifo, "oilp:134.2\n")
        os.write(self.fifo, "vbat:13.4\n")
        os.write(self.fifo, "lamb:0.89\n") 
        os.write(self.fifo, "lspd:45.2\n")
        os.write(self.fifo, "rspd:45.4\n")
        os.write(self.fifo, "rpm_:9500\n")
        os.write(self.fifo, "accx:0.87\n") 
        os.write(self.fifo, "accy:1.04\n")
        os.write(self.fifo, "accz:0.08\n")
        
        while (True):
            # print("In Loop: ")
            if (self.serial_port.inWaiting()>0): #if incoming bytes are waiting to be read from the serial input buffer
                data_str = self.serial_port.read(self.serial_port.inWaiting())
                self.parse_data(data_str)
                
            time.sleep(0.01)

    def parse_data(self, data_str):
        try: 
            key = data_str[:5]
            value_str = data_str[5:]
            print(key + "->" + value_str)

            value = float(value_str)
            print("(int)" + str(value))
            if(0 <= value <= 10e6): # Hopefully only good values get through? 
                if(key == "lf00:"):
                    os.write(self.fifo, "ctmp:" + str(value) + "\n")
                elif(key == "hf00:"):
                    os.write(self.fifo, "oilp:" + str(value) + "\n")
                elif(key == "lf01:"):
                    os.write(self.fifo, "lamb:" + str(value) + "\n")
                elif(key == "hf01:"):
                    os.write(self.fifo, "vbat:" + str(value) + "\n")
                elif(key == "lf02:"):
                    os.write(self.fifo, "lspd:" + str(value) + "\n")
                elif(key == "hf02:"):
                    os.write(self.fifo, "rspd:" + str(value) + "\n")
                elif(key == "lf03:"):
                    os.write(self.fifo, "rpm_:" + str(value) + "\n")
                elif(key == "hf03:"):
                    os.write(self.fifo, "accx:" + str(value) + "\n")
                elif(key == "lf04:"):
                    os.write(self.fifo, "accy:" + str(value) + "\n")
                elif(key == "hf04:"):
                    os.write(self.fifo, "accz:" + str(value) + "\n")
                else:
                    print("Unknown Code" + key + str(value))

        except Exception:
            traceback.print_exc(file=sys.stdout)
            

    def shutdown(self):
        print("Shutdown heard...exiting")
        os.close(self.fifo)
        os.remove(self.fifo_path)


if __name__ == '__main__':
    #try:
    m = Master()
    #except (KeyboardInterrupt, SystemExit):
    # l.shutdown()
    # sys.exit(0)

