import serial as s
import params as p
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
        os.write(self.fifo, "Pipe Open\n")

        self.serial_port = s.Serial('/dev/ttyAMA3', 115200, timeout=1) # Serial Baud rate from Arduino is 115200
        print("Got serial from Arduino")
        
        self.parse_data("l700:100.0\n")
        self.parse_data("h700:134.2\n")
        self.parse_data("l701:13.4\n") 
        self.parse_data("h701:0.98\n")
        self.parse_data("l702:45.2\n") # Spec swithced. RPM is now 702l (not reflected in all code)
        self.parse_data("h702:45.4\n")
        self.parse_data("l703:95000\n")
        self.parse_data("h703:0.87\n") 
        self.parse_data("l704:1.04\n")
        self.parse_data("h704:0.08\n")

        for rpm in range(p.MIN_RPM, p.REDLINE_RPM, 50):
            time.sleep(0.02)
            self.parse_data("l702:" + str(rpm * 10) + "\n")
        for rpm in range(p.REDLINE_RPM, p.MIN_RPM-1000, -100):
            time.sleep(0.02)
            self.parse_data("l702:" + str(rpm * 10) + "\n")

        self.parse_data("l703:0\n")
        
        while (True):
            # print("In Loop: ")
            if (self.serial_port.inWaiting()>0): #if incoming bytes are waiting to be read from the serial input buffer
                data_str = self.serial_port.readline()
                self.parse_data(data_str)
                
            time.sleep(0.01)

    def parse_data(self, data_str):
        try: 
            data_str = data_str.strip()
            print("Parsing: '{}'".format(data_str))

            key = data_str[:5]
            value_str = data_str[5:11]
            print(key + "->" + value_str)

            stripped = value_str.strip()

            print("(stripped)" + repr(stripped))
            value = float(stripped)
            print("(float)" + repr(value))
            # if(0 <= value <= 10e6): # Hopefully only good values get through? 
            if(key == "l700:"):
                os.write(self.fifo, "ctmp:" + str(value) + "\n")
            elif(key == "h700:"):
                value = round(((value / 1000.0) * 0.145), 2)
                os.write(self.fifo, "oilp:" + str(value) + "\n")
            elif(key == "l701:"):
                os.write(self.fifo, "vbat:" + str(value) + "\n")
            elif(key == "h701:"):
                os.write(self.fifo, "lamb:" + str(value) + "\n")
            elif(key == "l703:"):
                os.write(self.fifo, "lspd:" + str(value) + "\n")
            elif(key == "h703:"):
                os.write(self.fifo, "rspd:" + str(value) + "\n")
            elif(key == "l702:"):
                value = value / 10
                os.write(self.fifo, "rpm_:" + str(value) + "\n")
                print("Sending {} to leds".format(value))
                self.l.displayRPM(value)
            elif(key == "h702:"):
                os.write(self.fifo, "accx:" + str(value) + "\n")
            elif(key == "l704:"):
                os.write(self.fifo, "accy:" + str(value) + "\n")
            elif(key == "h704:"):
                # Up
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
    m = Master()
