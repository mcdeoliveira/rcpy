import rcpy
from rcpy._gpio_mmap import *

# definitions
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

DEBOUNCE_INTERVAL = 0.5

import io, threading, time, os
import select

class InputTimeout(Exception):
    pass

def read(pin, timeout = None, pipe = None):

    # create pipe if necessary
    destroy_pipe = False
    if pipe is None:
        pipe = rcpy.create_pipe()
        destroy_pipe = True
    
    # open stream
    filename = SYSFS_GPIO_DIR + '/gpio{}/value'.format(pin)
    
    with open(filename, 'rb', buffering = 0) as f:

        # create poller
        poller = select.poll()
        f.read()
        poller.register(f,
                        select.POLLPRI | select.POLLHUP | select.POLLERR)

        # listen to state change as well
        state_r_fd, state_w_fd = pipe
        poller.register(state_r_fd,
                        select.POLLIN | select.POLLHUP | select.POLLERR)

        while rcpy.get_state() != rcpy.EXITING:

            # wait for events
            if timeout:
                # can fail if timeout is given
                events = poller.poll(timeout)
                if len(events) == 0:
                    # destroy pipe
                    if destroy_pipe:
                        rcpy.destroy_pipe(pipe)
                    # raise timeout exception
                    raise InputTimeout('Input did not change in more than {} ms'.format(timeout))
                
            else:
                # timeout = None, never fails
                events = poller.poll()

            for fd, flag in events:

                # state change
                if fd is state_r_fd:
                    # get state
                    state = int(os.read(state_r_fd, 1))
                    if state == rcpy.EXITING:
                        # exit!
                        if destroy_pipe:
                            rcpy.destroy_pipe(pipe)
                        return

                # input event
                if fd is f.fileno():
                    # Handle inputs
                    if flag & (select.POLLIN | select.POLLPRI):
                        # destroy pipe
                        if destroy_pipe:
                            rcpy.destroy_pipe(pipe)
                        # return read value
                        return get(pin)
                
                    elif flag & (select.POLLHUP | select.POLLERR):
                        # destroy pipe
                        if destroy_pipe:
                            rcpy.destroy_pipe(pipe)
                        # raise exception
                        raise Exception('Could not read pin {}'.format(pin))

        # destroy pipe
        if destroy_pipe:
            rcpy.destroy_pipe(pipe)
                    
class Output:
    pass
                
class Input:

    def __init__(self, pin):
        self.pin = pin
    
    def is_high(self):
        return get(self.pin) == HIGH

    def is_low(self):
        return get(self.pin) == LOW

    def high_or_low(self, debounce = 0, timeout = None, pipe = None):
        
        # repeat until event is detected
        while rcpy.get_state() != rcpy.EXITING:

            # read event
            event = read(self.pin, timeout, pipe)

            # debounce
            k = 0
            value = event
            while k < debounce and value == event:
                time.sleep(DEBOUNCE_INTERVAL/1000)
                value = get(self.pin)
                k += 1
                
            # check value
            if value == event:
                return value
                    
    def high(self, debounce = 0, timeout = None, pipe = None):
        event = self.high_or_low(debounce, timeout, pipe)
        if event == HIGH:
            return True
        else:
            return False

    def low(self, debounce = 0, timeout = None, pipe = None):
        event = self.high_or_low(debounce, timeout, pipe = None)
        if event == LOW:
            return True
        else:
            return False

class InputEvent(threading.Thread):

    LOW = 1
    HIGH = 2
    
    class InputEventInterrupt(Exception):
        pass
    
    def __init__(self, input, event, debounce = 0, timeout = None, 
                 target = None, vargs = (), kwargs = {}):

        super().__init__()
        
        self.input = input
        self.event = event
        self.target = target
        self.vargs = vargs
        self.kwargs = kwargs
        self.timeout = timeout
        self.debounce = 0
        self.pipe = rcpy.create_pipe()

    def action(self, event):
        if self.target:
            # call target
            self.target(self.input, event, *self.vargs, **self.kwargs)
        else:
            # just check for valid event
            if event != InputEvent.HIGH and event != InputEvent.LOW:
                raise Exception('Unkown InputEvent {}'.format(event))
            
    def run(self):
        self.run = True
        while rcpy.get_state() != rcpy.EXITING and self.run:

            try:
                evnt = self.input.high_or_low(self.debounce,
                                              self.timeout,
                                              self.pipe)
                if evnt is not None:
                    evnt = 1 << evnt
                    if evnt & self.event:
                        # fire callback
                        self.action(evnt)
                        
            except InputTimeout:
                self.run = False

    def stop(self):
        self.run = False
        # write to pipe to abort
        os.write(self.pipe[1], bytes(str(rcpy.EXITING), 'UTF-8'))
        # sleep and destroy pipe
        time.sleep(1)
        rcpy.destroy_pipe(self.pipe)
        self.pipe = None
        
