from rcpy._gpio_mmap import *

# definitions

ON = 1
OFF = 0

HIGH = 1
LOW = 0

# direction
IN  = 0
OUT = 1

# edge
EDGE_NONE    = 0
EDGE_RISING  = 1
EDGE_FALLING = 2
EDGE_BOTH    = 3

# input pins
PAUSE_BTN         = 69 	# gpio2.5 P8.9
MODE_BTN          = 68	# gpio2.4 P8.10
IMU_INTERRUPT_PIN = 117 # gpio3.21 P9.25

# gpio output pins 
RED_LED     = 66 # gpio2.2  P8.7
GRN_LED     = 67 # gpio2.3  P8.8
MDIR1A      = 60 # gpio1.28 P9.12
MDIR1A_BLUE = 64 # gpio2.0 pin T13
MDIR1B      = 31 # gpio0.31 P9.13
MDIR2A      = 48 # gpio1.16 P9.15
MDIR2B      = 81 # gpio2.17 P8.34
MDIR2B_BLUE = 10 # gpio0.10 P8_31
MDIR4A      = 70 # gpio2.6  P8.45
MDIR4B      = 71 # gpio2.7  P8.46
MDIR3B      = 72 # gpio2.8  P8.43
MDIR3A      = 73 # gpio2.9  P8.44
MOT_STBY    = 20 # gpio0.20 P9.41
DSM_PIN     = 30 # gpio0.30 P9.11
SERVO_PWR   = 80 # gpio2.16 P8.36

SPI1_SS1_GPIO_PIN = 113 # gpio3.17	P9.28 
SPI1_SS2_GPIO_PIN = 49  # gpio1.17	P9.23 

# BB Blue GPIO OUT
BLUE_GP0_PIN_4 = 49 #  gpio 1_17 pin P9.23

# Battery Indicator LEDs
BATT_LED_1 = 27      #  P8.17
BATT_LED_2 = 65      #  P8.18
BATT_LED_2_BLUE = 11 #  different on BB Blue
BATT_LED_3 = 61      #  P8.26
BATT_LED_4 = 26      #  P8.14

SYSFS_GPIO_DIR = '/sys/class/gpio'
POLL_TIMEOUT = 100

DEBOUNCE_INTERVAL = 0.0005

import io
import select

def read(pin):
    
    # open stream
    filename = SYSFS_GPIO_DIR + '/gpio{}/value'.format(pin)
    
    with open(filename, 'rb') as f:

        # read first
        f.read()
        
        # create poller
        poller = select.poll()
        poller.register(f, select.POLLPRI | select.POLLHUP | select.POLLERR)

        while True:

            # wait for events
            events = poller.poll(POLL_TIMEOUT)
            
            for fd, flag in events:
                
                # Handle inputs
                if flag & (select.POLLIN | select.POLLPRI):
                    # return read value
                    return get(pin)
                elif flag & (select.POLLHUP | select.POLLERR):
                    raise Exception('Could not read pin {}'.format(pin))

class Input:

    def __init__(self, pin):
        self.pin = pin
    
    def is_high(self):
        return gpio.get(self.pin) == gpio.HIGH

    def is_low(self):
        return gpio.get(self.pin) == gpio.LOW

    def high_or_low(self, debounce = 0):
        
        # repeat until event is detected
        while True:

            # read event
            event = gpio.read(self.pin)
            
            # debounce
            k = 0
            value = event
            while k < debounce and value == event:
                time.sleep(DEBOUNCE_INTERVAL)
                value = gpio.get(self.pin)
                k += 1
                
            # check value
            if value == event:
                return value
                    
    def high(self, debounce = 0):
        if high_or_low(self, debounce) == gpio.HIGH:
            return True
        else:
            return False

    def low(self, debounce = 0):
        if high_or_low(self, debounce) == gpio.LOW:
            return True
        else:
            return False

class InputEvent(threading.Thread):

    class InputEventInterrupt(Exception):
        pass
    
    def __init__(self, input, event):

        super().__init__()
        
        self.input = input
        self.event = event

    def action(self, event, *vargs, **kwargs):
        pass
        
    def run(self):
        self.run = True
        while rcpy.get_state() != rcpy.EXITING and self.run:

            try:
                evnt = self.input.high_or_low()
                if evnt & self.event:
                    # fire callback
                    self.action(evnt)
            except InputEvent.InputEventInterrupt:
                self.run = False

    def stop(self):
        self.run = False

