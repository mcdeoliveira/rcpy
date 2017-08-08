import rcpy
import rcpy.gpio as gpio
import rcpy.clock as clock

import threading, time

ON = gpio.HIGH
OFF = gpio.LOW

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
        gpio.set(self.pin, ON)

    def off(self):
        self.state = OFF
        gpio.set(self.pin, OFF)

    def toggle(self):
        if self.state == ON:
            self.off()
        else:
            self.on()

    run = toggle
            
    def blink(self, period):
        thread = Blink(self, period)
        thread.start()
        return thread

    
# define leds
red = LED(gpio.RED_LED)
green = LED(gpio.GRN_LED)
