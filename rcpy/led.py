import rcpy
import rcpy.clock as clock
from rcpy._led import *

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

    def __init__(self, pin, state = OFF):

        self.pin = pin
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
        set(self.pin, ON)

    def off(self):
        self.state = OFF
        set(self.pin, OFF)

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
green = 0
red = 1

