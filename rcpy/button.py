import rcpy
import rcpy.gpio as gpio

import threading
import time

class Button():

    def __init__(self, pin):
        self.pin = pin
    
    def is_pressed(self):
        return gpio.get(self.pin) == gpio.LOW

    def is_released(self):
        return gpio.get(self.pin) == gpio.HIGH
    
    def pressed(self, callback):
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

    def released(self, callback):
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
