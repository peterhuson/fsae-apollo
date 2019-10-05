import serial as s
import params as p
import sys, traceback, os, time
from leds import LEDs
 
class Master:
    def __init__(self):
        self.l = LEDs()
        print("got an LED handler!")

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
        if (self.serial_port.inWaiting()>0): #if incoming bytes are waiting to be read from the serial input buffer
            pass
        else: 
            self.fake_data()
        
        while (True):
            # print("In Loop: ")
            if (self.serial_port.inWaiting()>0): #if incoming bytes are waiting to be read from the serial input buffer
                data_str = self.serial_port.readline()
                self.parse_data(data_str)
                
            time.sleep(0.01)

    def fake_data(self):
        ### Show some fake data to excersize the screen ###
        self.parse_data("l700:55.69\n") # ctmp
        self.parse_data("h700:3000\n") # oilp (pascals)
        self.parse_data("l701:11.9\n") # vbat
        self.parse_data("h701:1.1\n") # lambda
        self.parse_data("l702:0\n") # RPM 
        self.parse_data("h702:10\n") # TPS
        self.parse_data("l703:95\n") # lspd
        self.parse_data("h703:2\n") # rspd
        self.parse_data("l704:9.814\n") #accy
        self.parse_data("h704:0.08\n") #accz

        for rpm in range(0, p.REDLINE_RPM, 100):
            time.sleep(0.01)
            self.parse_data("l702:" + str(rpm * 10) + "\n")
        for rpm in range(p.REDLINE_RPM, 0, -100):
            time.sleep(0.01)
            self.parse_data("l702:" + str(rpm * 10) + "\n")

        for lspd in range(80, 0, -2):
            time.sleep(0.01)
            print(lspd)
            self.parse_data("l703:" + str(lspd) + "\n")

        self.parse_data("l703:0\n")

    def parse_data(self, data_str):
        last_rpm = 0.
        last_rspd = 0.

        try: 
            data_str = data_str.strip()
            # print("Parsing: '{}'".format(data_str))

            key = data_str[:5]
            value_str = data_str[5:11]
            print(key + "->" + value_str)

            stripped = value_str.strip()

            value = float(stripped)
            # print("(float)" + repr(value))
            # if(0 <= value <= 10e6): # Hopefully only good values get through? 
            if(key == "l700:"):
                value = int(value)
                os.write(self.fifo, "ctmp:" + str(value) + "\n")
            elif(key == "h700:"):
                value = int((value / 1000.0) * 0.145)
                os.write(self.fifo, "oilp:" + str(value) + "\n")
            elif(key == "l701:"):
                value = round(value, 1)
                os.write(self.fifo, "vbat:" + str(value) + "\n")
            elif(key == "h701:"):
                value = round(value, 1)
                os.write(self.fifo, "lamb:" + str(value) + "\n")
            elif(key == "l703:"):
                value = int(round(value, 0))
                # print("Sending {} to lspd".format(value))
                os.write(self.fifo, "lspd:" + str(value) + "\n")
            elif(key == "h703:"):
                value = round(value, 0)
                last_rspd = value
                os.write(self.fifo, "rspd:" + str(int(value)) + "\n")
                self.calculate_gear_position(last_rspd, last_rpm)
            elif(key == "l702:"):
                value = int((value / (2*3.14)))
                last_rpm = value
                os.write(self.fifo, "rpm_:" + str(value) + "\n")
                # print("Sending {} to leds".format(value))
                self.l.displayRPM(value)
            elif(key == "h702:"):
                value = round(value, 0)
                os.write(self.fifo, "tps_:" + str(value) + "\n")
            elif(key == "l704:"):
                value = round((value / p.GRAVITY), 2)
                os.write(self.fifo, "accy:" + str(value) + "G\n")
            elif(key == "h704:"):
                # Up
                value = round((value / p.GRAVITY), 2)
                os.write(self.fifo, "accz:" + str(value) + "G\n")
            else:
                print("Unknown Code" + key + str(value))

        except Exception:
            traceback.print_exc(file=sys.stdout)

        # Translate the ratio between wheelspeed and RPM, then send a guess at gear position    
    def calculate_gear_position(self, wheelspeed, rpm):
        pass

    def shutdown(self):
        print("Shutdown heard...exiting")
        os.close(self.fifo)
        os.remove(self.fifo_path)


if __name__ == '__main__':
    m = Master()
