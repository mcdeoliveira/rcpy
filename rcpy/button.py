import rcpy
import rcpy.gpio as gpio

import threading
import time

DEBOUNCE = 3
PRESSED = gpio.LOW
RELEASED = gpio.HIGH
    
class ButtonEvent(gpio.InputEvent):

    PRESSED = gpio.InputEvent.LOW
    RELEASED = gpio.InputEvent.HIGH

class Button(gpio.Input):

    def is_pressed(self, debounce = DEBOUNCE, timeout = gpio.POLL_TIMEOUT):
        return self.is_low(debounce, timeout)

    def is_released(self, debounce = DEBOUNCE, timeout = gpio.POLL_TIMEOUT):
        return self.is_high(debounce, timeout)
    
    def pressed_or_released(self, debounce = DEBOUNCE, timeout = gpio.POLL_TIMEOUT):
        return self.high_or_low(debounce, timeout)
                    
    def pressed(self, debounce = DEBOUNCE, timeout = gpio.POLL_TIMEOUT):
        return self.low(debounce, timeout)

    def released(self, debounce = DEBOUNCE, timeout = gpio.POLL_TIMEOUT):
        return self.high(debounce, timeout)
        
# definitions

# BUTTONs
pause = Button(gpio.PAUSE_BTN)
mode = Button(gpio.MODE_BTN)
