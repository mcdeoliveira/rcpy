import rcpy
from . import clock
from . import gpio

import threading, time

ON = 1
OFF = 0

class Blink(clock.Clock):

    def __init__(self, led, period):

        # call super
        super().__init__(led, period)

    def stop(self):

        # call super
        super().stop()

        # turn off
        time.sleep(2*self.period)
        self.action.off()

class LED(clock.Action):

    def __init__(self, chip, line, state = OFF):

        self.output = gpio.Output(chip, line)
        if state == ON:
            self.on()
        else:
            self.off()

    def is_on(self):
        return self.state == ON

    def is_off(self):
        return self.state == OFF

    def on(self):
        self.state = ON
        self.output.set(ON)

    def off(self):
        self.state = OFF
        self.output.set(OFF)

    def toggle(self):
        if self.state == ON:
            self.off()
        else:
            self.on()

    run = toggle

    def blink(self, period):
        thread = blink(self, period)
        thread.start()
        return thread


# define leds
red = LED(*gpio.RED_LED)
green = LED(*gpio.GRN_LED)
