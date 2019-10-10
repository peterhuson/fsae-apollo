from display import params

class LEDController:
    def __init__(self):
        self.num_steps = params.NUM_LEDS // 2
        self.step_width = (params.SHIFT_RPM - params.LED_MIN_RPM) // self.num_steps

    def display_rpm(self):
        ...

    def