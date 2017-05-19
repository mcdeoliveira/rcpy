import rcpy
import rcpy.gpio as gpio

import threading

class LED:

    def __init__(self, pin, state = gpio.OFF):

        self.condition = threading.Condition()
        self.pin = pin
        if state == gpio.ON:
            self.on()
        else:
            self.off()

    def on(self):
        self.state = gpio.ON
        gpio.set(self.pin, gpio.ON)

    def off(self):
        self.state = gpio.OFF
        gpio.set(self.pin, gpio.OFF)

    def toggle(self):
        if self.state == gpio.ON:
            self.off()
        else:
            self.on()

    def _blink(self):

        # Acquire lock
        self.condition.acquire()

        # Toggle
        self.toggle()
        
        # Notify lock
        self.condition.notify_all()

        # Release lock
        self.condition.release()
        
            
    def blink(frequency):

        self.run = True
        while rcpy.get_state() != rcpy.EXITING and self.run:

            # Acquire condition
            self.condition.acquire()
            
            # Setup timer
            self.timer = threading.Timer(self.period, self._blink)
            self.timer.start()

            # Wait 
            self.condition.wait()

            # and release
            self.condition.release()

# define leds
red = LED(gpio.RED_LED)
green = LED(gpio.GRN_LED)
