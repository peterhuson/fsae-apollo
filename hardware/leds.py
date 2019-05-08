# from driver import apa102
from apa102_led import apa102
import params as p
import time, sys
import numpy as np

NUM_LED = 13
MOSI = 10
SCLK = 11

class LEDs:
    def __init__(self):
        self.strip = apa102.APA102(num_led=p.NUM_LED, mosi=MOSI, sclk=SCLK,order='rgb')
        self.strip.clear_strip()
        self.num_steps = (p.NUM_LED / 2) + 1
        self.step_width = (p.MAX_RPM - p.MIN_RPM) / self.num_steps


    def displayRPM(self, RPM):
        RPM = int(RPM)

        if RPM > p.MAX_RPM: # Flash Red
            self.setall(p.RED, p.BRIGHTNESS_PERCENTAGE + 50)
            return
        elif RPM < p.MIN_RPM: # Below MIN_RPM the side-most lights will slowly ramp brightness
            brightness = int(p.BRIGHTNESS_PERCENTAGE * ((RPM * 1.) / p.MIN_RPM))
            self.strip.set_pixel_rgb(0, p.GREEN, brightness)
            self.strip.set_pixel_rgb(12, p.GREEN, brightness)
            self.strip.show()
            return 
        elif p.MIN_RPM <= RPM <= p.MAX_RPM:
            leds_to_change = np.copy(p.led_map)

            step = (RPM - p.MIN_RPM) / self.step_width
            leds_to_change[p.led_map[:, 0] > step] = [0, 0, p.OFF]

            self.updateLeds(leds_to_change)
        else: 
            print("RPM value {} could not be displayed".format(RPM))

    def updateLeds(self, update_map):
        for i, elem in enumerate(update_map):
            self.strip.set_pixel_rgb(i,elem[2], p.BRIGHTNESS_PERCENTAGE)
        self.strip.show()

    def setall(self, color, brightness):
        for i in range(p.NUM_LED):
            self.strip.set_pixel_rgb(i,color, brightness)
        self.strip.show()

    def shutdown(self):
        print("received shutdown command")
        self.strip.clear_strip()
        self.strip.cleanup()

    def rainbow(self):
        for brightness in range(0, 40, 5):
            self.setall(RED, brightness)
            time.sleep(0.2)
            self.setall(ORANGE, brightness)
            time.sleep(0.2)
            self.setall(YELLOW, brightness)
            time.sleep(0.2)
            self.setall(GREEN, brightness)
            time.sleep(0.2)
            self.setall(BLUE, brightness)
            time.sleep(0.2)
            self.setall(PURPLE, brightness)
            time.sleep(0.2)

        # self.strip.set_pixel_rgb(0,RED)
        # self.strip.show()
        # time.sleep(0.1)
        # self.strip.set_pixel_rgb(1,RED)
        # self.strip.show()
        # time.sleep(0.1)
        # self.strip.set_pixel_rgb(2,RED)
        # self.strip.show()
        # time.sleep(0.1)
        # self.strip.set_pixel_rgb(0,GREEN)
        # self.strip.show()
        # time.sleep(0.1)
        # self.strip.set_pixel_rgb(1,GREEN)
        # self.strip.show()
        # time.sleep(0.1)
        # self.strip.set_pixel_rgb(2,GREEN)
        # self.strip.show()
        # time.sleep(0.1)
        # self.strip.set_pixel_rgb(0,OFF)
        # self.strip.show()
        # time.sleep(0.1)
        # self.strip.set_pixel_rgb(1,OFF)
        # self.strip.show()
        # time.sleep(0.1)
        # self.strip.set_pixel_rgb(2,OFF)
        # self.strip.show()
        # time.sleep(0.1)

        print("rainbow test complete")

if __name__ == '__main__':
    #try:
    l = LEDs()
    #except (KeyboardInterrupt, SystemExit):
    # l.shutdown()
    # sys.exit(0)

