from multiprocessing import Process, Pipe
from display.leds import LEDController
from display.screen import ScreenController
import argparse


def runDataReceiving():
    pass


def runDisplay():
    pass


def runSteeringWheel():
    # create process for display and data reception
    dataReceiving = Process(target=runDataReceiving())
    display = Process(target=runDisplay)

    dataReceiving.start()
    display.start()
    
    # don't finish while dataReceiving and display are running
    dataReceiving.join()
    display.join()

    # close out the pipe once the processes are done
    writer.close()
    reader.close()


def parse_args():
    # Helper function to only allow positive pin numbers
    taken_pins = []  # Keeps track of pins that are taken so there are no collisions

    def check_valid_pin(value):
        pin_value = int(value)

        if pin_value < 0:
            raise argparse.ArgumentTypeError(f"{pin_value} is an invalid pin number")
        if pin_value in taken_pins:
            raise argparse.ArgumentParser(f"Pin {pin_value} is already taken")

        return pin_value

    def check_valid_num_leds(value):
        num_leds_value = int(value)

        if num_leds_value < 1:
            raise argparse.ArgumentTypeError(f"Must be 1 or more LEDs; given {num_leds_value}")

        return num_leds_value

    parser = argparse.ArgumentParser()
    # Parse number of LEDs
    parser.add_argument("num_leds", type=check_valid_num_leds,
                        help="Number of LEDs for the rpm indicator")
    # Parse pin numbers for LED strip
    pin_group = parser.add_argument_group("pinGroup")
    pin_group.add_argument("data_pin", type=check_valid_pin,
                           help="The pin where the data channel (MOSI) is plugged in")
    pin_group.add_argument("clock_pin", type=check_valid_pin,
                           help="The pin where the serial clock channel (SCLK) is plugged in")
    # Optional flag to use stub data source
    parser.add_argument("--debug-data", action="store_true")

    # Actually parse the data
    return parser.parse_args()



if __name__ == "__main__":
    runSteeringWheel()
