from driver import apa102
import time, sys

OFF = 0x000000 #Off
RED = 0xFF0000 #Red
ORANGE = 0xFF7F00 #Orange
YELLOW = 0xFFFF00 #Yellow
GREEN = 0x00FF00 #Green
BLUE = 0x0000FF #Blue
PURPLE = 0x4B0082 #Indigo
VIOLET = 0x9400D3 #Violet

NUM_LED = 15
MOSI = 10
SCLK = 11

class LEDs:
	def __init__(self):
		self.strip = apa102.APA102(num_led=NUM_LED, mosi=MOSI, sclk=SCLK,order='rgb')
		self.strip.clear_strip()
		self.rainbow()

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

		self.strip.clear_strip()
		self.strip.cleanup()


	def setall(self, color, brightness):
		for i in range(p.num_leds):
			self.strip.set_pixel_rgb(i,color)
		self.strip.show()

	def shutdown(self):
		print("received shutdown command")
		self.strip.clear_strip()
		self.strip.cleanup()

	def rainbow(self):
		for brightness in range(0, 100, 20):
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

		print "rainbow test complete"

if __name__ == '__main__':
	try:
		l = LEDs()
	except (KeyboardInterrupt, SystemExit):
        l.shutdown()
		sys.exit(0)

