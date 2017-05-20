import rcpy
import rcpy.gpio as gpio

import threading, time

ON = gpio.HIGH
OFF = gpio.LOW

class Blink(threading.Thread):

    def __init__(self, led, period):

        super().__init__()
        
        self.condition = threading.Condition()
        self.led = led
        self.period = period
        self._suspend = False

    def set_period(self, period):
        self.period = period

    def toggle(self):
        self._suspend = not self._suspend
        
    def _blink(self):

        # Acquire lock
        self.condition.acquire()

        # Toggle
        if not self._suspend:
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
        time.sleep(2*self.period)
        self.led.off()

class LED:

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

    def blink(self, period):
        thread = Blink(self, period)
        thread.start()
        return thread

    
# define leds
red = LED(gpio.RED_LED)
green = LED(gpio.GRN_LED)
