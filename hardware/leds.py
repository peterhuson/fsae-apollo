# from driver import apa102
from apa102_led import apa102
import params as p
import time, sys
import numpy as np

NUM_LED = 13
MOSI = 10
SCLK = 11

MAX_RPM = 13000
MIN_RPM = 8000

class LEDs:
	def __init__(self):
		self.strip = apa102.APA102(num_led=NUM_LED, mosi=MOSI, sclk=SCLK,order='rgb')
		self.strip.clear_strip()
		#try:
			# self.rainbow()
		#except: 
		#	self.shutdown()
		# print("Brightness 0-100")
		# for a in range(0,10):
		# 	for b in range(0,100):
		# 			strip.set_pixel_rgb(0,0xFF0000, b) #Red
		# 			strip.set_pixel_rgb(1,0xFF7F00, b) #Orange
		# 			strip.set_pixel_rgb(2,0xFFFF00, b) #Yellow
		# 			strip.set_pixel_rgb(3,0x00FF00, b) #Green
		# 			strip.set_pixel_rgb(4,0x0000FF, b) #Blue
		# 			strip.set_pixel_rgb(5,0x4B0082, b) #Indigo
		# 			strip.set_pixel_rgb(6,0x9400D3, b) #Violet
		# 			strip.show()
		# 			time.sleep(0.03)

		#self.strip.clear_strip()
		#self.strip.cleanup()

	def displayRPM(self, RPM):
		num_steps = (NUM_LED / 2) + 1
		step_width = (MAX_RPM - MIN_RPM) / num_steps
		step = (RPM - MIN_RPM) / step_width
		print("{} RPM calculated as step {}".format(RPM, step))

		leds_to_change = p.led_map
		leds_to_change[p.led_map[:, 0] > step] = [0, 0, p.BLUE] # TODO p.OFF
		print("LEDs to change: {}".format(leds_to_change))

		self.updateLeds(leds_to_change)

	def updateLeds(self, update_map):
		for i, elem in enumerate(update_map):
			print("setting {} to {}".format(i, elem[2]))
			self.strip.set_pixel_rgb(i,elem[2], 1)
		self.strip.show()

	def setall(self, color, brightness):
		for i in range(NUM_LED):
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

