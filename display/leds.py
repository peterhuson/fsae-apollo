from display import params


class LEDController:
    def __init__(self, num_leds, data_pin, clock_pin):
        # TODO: intialize the led strip here
        self.num_steps = num_leds // 2
        self.step_width = (params.SHIFT_RPM - params.LED_MIN_RPM) // self.num_steps

    def get_led_color(self, led_id):
        ...

    def display_rpm(self, rpm):
        ...

    def flash_color(self, color, duration):
        ...
