import serial as s
import sys, traceback, os, time
from leds import LEDs
 
class Master:
    def __init__(self):
        self.l = LEDs()
        self.l.displaycoolant_temp(8500)
        print("got an LED handler!")

        # self.serial_port = s.Serial('/dev/tty.Bluetooth-Incoming-Port', 9600, timeout=1) # Default Serial Baud rate is 9600
        
        self.serial_port = s.Serial('/dev/ttyAMA3', 9600, timeout=1) # Default Serial Baud rate is 9600
        self.serial_port.write(b'+++')
        ret = self.serial_port.readline()
        print(ret)
        # self.serial_port.write(b'AT+C=18\n') # Set CanBus rate to 1Mb/s
        self.serial_port.write(b'AT+C=13\n') # Set CanBus rate to 125Kb/s
        ret = self.serial_port.readline()
        print(ret)
        self.serial_port.write(b'AT+Q\n')
        ret = self.serial_port.readline()
        print(ret)
        time.sleep(0.1)

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


        self.serial_port = s.Serial('/dev/ttyAMA3', 115200, timeout=1) # Default Serial Baud rate is 9600
        while (True):
        
            if (self.serial_port.inWaiting()>0): #if incoming bytes are waiting to be read from the serial input buffer
                data_str = self.serial_port.read(self.serial_port.inWaiting())
                 
                key = data_str[:5]
                value = data_str[5:]
		        print(key + "->" + value)
                # if(key == "ctmp:"):
                    
                # if(key == "oilp:"):

                # if(key == "vbat:"):
                # if(key == "lamb:"):

                # if(key == "lspd:"):
                # if(key == "rspd:"):

                if(key == "rpm_:"):
                    
                    print("sending {} to leds".format(value))
                    self.l.displaycoolant_temp(value)

                # if(key == "accx:"):

                # if(key == "accy:"):
                # if(key == "accz:"):
                

        # if(canId == 0x700){
        #     float *ctmp;
        #     unsigned long coolant_temp;
        #     coolant_temp = (unsigned long) buf[3] + ((unsigned long) buf[2] << 8) + ((unsigned long) buf[1] << 16) + ((unsigned long) buf[0] << 24);
        #     ctmp = (float *)&coolant_temp;
        #     Serial.print("ctmp:");
        #     Serial.println(*ctmp);

        #     float *oilp;
        #     unsigned long oil_pressure;
        #     oil_pressure = (unsigned long) buf[7] + ((unsigned long) buf[6] << 8) + ((unsigned long) buf[5] << 16) + ((unsigned long) buf[4] << 24);
        #     oilp = (float *)&oil_pressure;
        #     Serial.print("oilp:");
        #     Serial.println(*oilp);
        # }

        # if(canId == 0x701){
            
        #     float *bv;
        #     unsigned long bat_voltage;
        #     bat_voltage = (unsigned long) buf[3] + ((unsigned long) buf[2] << 8) + ((unsigned long) buf[1] << 16) + ((unsigned long) buf[0] << 24);
        #     bv = (float *)&bat_voltage;
        #     Serial.print("vbat:");
        #     Serial.println(*bv);

        #     float *lam;
        #     unsigned long lambda;
        #     lambda = (unsigned long) buf[7] + ((unsigned long) buf[6] << 8) + ((unsigned long) buf[5] << 16) + ((unsigned long) buf[4] << 24);
        #     lam = (float *)&lambda;
        #     Serial.print("lamb:");
        #     Serial.println(*lam);
        # }


        # if(canId == 0x702){

        #     float *lspd;
        #     unsigned long left_speed;
        #     left_speed = (unsigned long) buf[3] + ((unsigned long) buf[2] << 8) + ((unsigned long) buf[1] << 16) + ((unsigned long) buf[0] << 24);
        #     lspd = (float *)&left_speed;
        #     Serial.print("lspd:");
        #     Serial.println(*lspd);
            
        #     float *rspd;
        #     unsigned long right_speed;
        #     right_speed = (unsigned long) buf[7] + ((unsigned long) buf[6] << 8) + ((unsigned long) buf[5] << 16) + ((unsigned long) buf[4] << 24);
        #     rspd = (float *)&right_speed;
        #     Serial.print("rspd:");
        #     Serial.println(*rspd);
        # }

        # if(canId == 0x703){

        #     float *rpm;
        #     unsigned long engine_rpm;
        #     engine_rpm = (unsigned long) buf[3] + ((unsigned long) buf[2] << 8) + ((unsigned long) buf[1] << 16) + ((unsigned long) buf[0] << 24);
        #     rpm = (float *)&engine_rpm;
        #     Serial.print("rpm_:");
        #     Serial.println(*rpm);
            
        #     float *accx;
        #     unsigned long x_acceleration;
        #     x_acceleration = (unsigned long) buf[7] + ((unsigned long) buf[6] << 8) + ((unsigned long) buf[5] << 16) + ((unsigned long) buf[4] << 24);
        #     accx = (float *)&x_acceleration;
        #     Serial.print("accx:");
        #     Serial.println(*accx);
        # }
        
        # if(canId == 0x704){
            
        #     float *accy;
        #     unsigned long y_acceleration;
        #     y_acceleration = (unsigned long) buf[3] + ((unsigned long) buf[2] << 8) + ((unsigned long) buf[1] << 16) + ((unsigned long) buf[0] << 24);
        #     accy = (float *)&y_acceleration;
        #     Serial.print("accy:");
        #     Serial.println(*accy);

        #     float *accz;
        #     unsigned long z_acceleration;
        #     z_acceleration = (unsigned long) buf[7] + ((unsigned long) buf[6] << 8) + ((unsigned long) buf[5] << 16) + ((unsigned long) buf[4] << 24);
        #     accz = (float *)&z_acceleration;
        #     Serial.print("accz:");
        #     Serial.println(*accz);
        # }

                # address = data_str[:4] # Get the first 4 bytes of data
                # print(address)

                # value = data_str[4:] # Get everything after the first 4 bytes
                # print(value)


                
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

