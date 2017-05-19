import rcpy
import rcpy.gpio as gpio

import threading

class Button():

    def __init__(self, pin):
        self.pin = pin
    
    def is_pressed(self):
        return gpio.get(self.pin)

    def pressed(self, callback):
        
    
# definitions

# BUTTONs
PAUSE  = 0
MODE = 1

# class for timeout
class TimeoutException(Exception):
    pass

# timeout handler
def timeout_handler(signum, frame):
    raise TimeoutException()

# pressed?
def pressed(button, timeout = 0):

    # set a timeout
    if timeout > 0:
        threading.Timer(timeout, timeout_handler)

    try:
        return _pressed(button)
    except TimeoutException:
        return False

# released?
def released(button, timeout = 0):

    # set a timeout
    if timeout > 0:
        threading.Timer(timeout, timeout_handler)
        
    try:
        return _released(button)
    except TimeoutException:
        return False
