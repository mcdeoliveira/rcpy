import rcpy
import rcpy.gpio as gpio

import threading, time

class Blink(threading.Thread):

    def __init__(self, led, period):

        super().__init__()
        
        self.condition = threading.Condition()
        self.led = led
        self.period = period
    
    def _blink(self):

        # Acquire lock
        self.condition.acquire()

        # Toggle
        self.led.toggle()
        
        # Notify lock
        self.condition.notify_all()

        # Release lock
        self.condition.release()
    
    def run(self):

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

    def stop(self):

        self.run = False;
        
        # Acquire lock
        self.condition.acquire()

        # Notify lock
        self.condition.notify_all()

        # Release lock
        self.condition.release()

        # turn off
        time.sleep(self.period)
        self.led.off()

class LED:

    def __init__(self, pin, state = gpio.OFF):

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

    def blink(self, period):
        thread = Blink(self, period)
        thread.start()
        return thread

    
# define leds
red = LED(gpio.RED_LED)
green = LED(gpio.GRN_LED)
