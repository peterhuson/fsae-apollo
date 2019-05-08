import numpy as np

NUM_LED = 13
MOSI = 10
SCLK = 11

GRAVITY = 9.81

WHEELRADIUS = 8

REDLINE_RPM = 13500
MAX_RPM = 13000
MIN_RPM = 7000
BRIGHTNESS_PERCENTAGE = 20

# DEFINE LED colors

OFF = 0x000000 #Off
RED = 0xFF0000 #Red
ORANGE = 0xFF7F00 #Orange
YELLOW = 0xFFFF00 #Yellow
GREEN = 0x00FF00 #Green
BLUE = 0x0000FF #Blue
PURPLE = 0x4B0082 #Indigo
VIOLET = 0x9400D3 #Violet

# DEFINE Colors of LEDs in RPM Slider 
# [step, num_led, color]
led_map = np.array([
    [0, 0, GREEN],
    [1, 1, GREEN], 
    [2, 2, GREEN], 
    [3, 3, ORANGE], 
    [4, 4, ORANGE], 
    [5, 5, RED], 
    [6, 6, RED], 
    [5, 7, RED], 
    [4, 8, ORANGE], 
    [3, 9, ORANGE], 
    [2, 10, GREEN], 
    [1, 11, GREEN], 
    [0, 12, GREEN], 
])