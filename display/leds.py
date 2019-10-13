from driver import apa102
from display import params
from display.params import LEDColor


class LEDController:
    def __init__(self, num_leds: int):
        self.strip = apa102.APA102(num_led=num_leds,  order="rgb",
                                   mosi=params.DATA_PIN, sclk=params.CLOCK_PIN)
        self.strip.clear_strip()

        self.num_steps = num_leds // 2
        self.step_width = (params.SHIFT_RPM - params.LED_MIN_RPM) // self.num_steps

    def get_led_std_color(self, led_id):
        ...

    def run_startup(self):
        # Run initialization sequence
        ...

    def flash_color(self, color: LEDColor, duration: int):
        # TODO: maybe flashing?
        ...

    def display_rpm(self, rpm):
        ...

