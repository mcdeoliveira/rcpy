import rcpy
import rcpy.gpio as gpio

import threading
import time

DEBOUNCE = 3
DEBOUNCE_INTERVAL = 0.0005

class ButtonEvent(threading.Thread):

    class ButtonEventInterrupt(Exception):
        pass
    
    def __init__(self, button, event):

        super().__init__()
        
        self.button = button
        self.event = event

    def action(self, *vargs, **kwargs):
        print('ACTION!')
        
    def run(self):
        self.run = True
        while rcpy.get_state() != rcpy.EXITING and self.run:

            try:
                if self.button.pressed_or_released() & self.event:
                    # fire callback
                    callback()
            except ButtonEvent.ButtonEventInterrupt:
                self.run = False

    def stop(self):
        
        raise ButtonEvent.ButtonEventInterrupt()

class Button():

    PRESSED = 1
    RELEASED = 2
    
    def __init__(self, pin):
        self.pin = pin
    
    def is_pressed(self):
        return gpio.get(self.pin) == gpio.LOW

    def is_released(self):
        return gpio.get(self.pin) == gpio.HIGH

    def pressed_or_released(self):
        
        # repeat until event is detected
        while True:

            # read event
            event = gpio.read(self.pin)

            # debounce
            k = 0
            value = event
            while k < DEBOUNCE and value == event:
                time.sleep(DEBOUNCE_INTERVAL)
                value = gpio.get(self.pin)
                k += 1
                # check value
                if value == event:
                    if value == gpio.LOW:
                        return PRESSED
                    else:
                        return RELEASED
                    
    def pressed(self):
        value = gpio.read(self.pin)
        # debounce
        k = 0
        while k < 3 and value == gpio.LOW:
            time.sleep(0.0005)
            value = gpio.get(self.pin)
            k += 1
        # check value
        if value == gpio.LOW:
            return True
        else:
            return False

    def released(self):
        value = gpio.read(self.pin)
        # debounce
        k = 0
        while k < 3 and value == gpio.HIGH:
            time.sleep(0.0005)
            value = gpio.get(self.pin)
            k += 1
        # check value
        if value == gpio.HIGH:
            return True
        else:
            return False
        
# definitions

# BUTTONs
pause = Button(gpio.PAUSE_BTN)
mode = Button(gpio.MODE_BTN)
