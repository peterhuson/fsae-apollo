from math import ceil
from time import sleep
from driver import apa102
from display import params
from display.params import LEDColor


class LEDController:
    def __init__(self, num_leds: int):
        self.strip = apa102.APA102(num_led=num_leds,  order="rgb",
                                   mosi=params.DATA_PIN, sclk=params.CLOCK_PIN)
        self.strip.clear_strip()

        self.num_leds = num_leds
        self.num_steps = ceil(num_leds / 2)
        self.step_width = (params.SHIFT_RPM - params.LED_MIN_RPM) // self.num_steps

    def get_led_std_color(self, led_id):
        step = led_id // 2  # 0-indexed step
        step_from_end = self.num_steps - step - 1  # 0-indexed

        if step_from_end / step <= 0.30 or step_from_end <= 1:
            return LEDColor.RED
        elif step_from_end / step <= 0.60:
            return LEDColor.ORANGE
        else:
            return LEDColor.GREEN

    def run_startup(self):
        # Run initialization sequence (run leds through rpm range up then down)
        for rev in range(params.LED_MIN_RPM, params.SHIFT_RPM, self.step_width):
            self.display_rpm(rev)
            sleep(0.1)

        for rev in range(params.SHIFT_RPM, params.LED_MIN_RPM, -self.step_width):
            self.display_rpm(rev)
            sleep(0.1)

    def flash_color(self, color: LEDColor, duration: int):
        for led in range(self.num_leds):
            self.strip.set_pixel_rgb(led, color.value, bright_percent=params.LED_BRIGHTNESS)

    def display_rpm(self, rpm):
        ...

