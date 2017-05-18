from rcpy.led import set, get
from rcpy.led import blink as _blink

import threading
import time

# definitions

# LEDs
GREEN  = 0
RED = 1

# state
ON  = 1
OFF = 0

def blink(led, hz):
    state = led.ON
    while True:
        set(led, state)
        state = not state
        time.sleep(1/hz)

def blink(led, hz, period):

    if period > 0:
        _blink(led, hz, period)
    
    elif period <= 0:
        thread = threading.Thread(target = blink,
                                  args = (led, hz))
        thread.start()
        return thread
