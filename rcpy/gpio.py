import rcpy

import sys
import gpiod

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
PAUSE_BTN         = (2, 5)  # gpio2.5 P8.9
MODE_BTN          = (2, 4)  # gpio2.4 P8.10
IMU_INTERRUPT_PIN = (3, 21) # gpio3.21 P9.25

# gpio output pins
RED_LED     = (2,2)  # gpio2.2  P8.7
GRN_LED     = (2,3)  # gpio2.3  P8.8
MDIR1A      = (1,28) # gpio1.28 P9.12
MDIR1A_BLUE = (2,0)  # gpio2.0 pin T13
MDIR1B      = (0,31) # gpio0.31 P9.13
MDIR2A      = (1,16) # gpio1.16 P9.15
MDIR2B      = (2,17) # gpio2.17 P8.34
MDIR2B_BLUE = (0,10) # gpio0.10 P8_31
MDIR4A      = (2,6)  # gpio2.6  P8.45
MDIR4B      = (2,7)  # gpio2.7  P8.46
MDIR3B      = (2,8)  # gpio2.8  P8.43
MDIR3A      = (2,9)  # gpio2.9  P8.44
MOT_STBY    = (0,20) # gpio0.20 P9.41
DSM_PIN     = (0,30) # gpio0.30 P9.11
SERVO_PWR   = (2,16) # gpio2.16 P8.36

SPI1_SS1_GPIO_PIN = (3,17) # gpio3.17 P9.28
SPI1_SS2_GPIO_PIN = (1,17) # gpio1.17 P9.23

# BB Blue GPIO OUT
BLUE_GP0_PIN_4 = (1,17)    # gpio1.17 P9.23

# Battery Indicator LEDs
BATT_LED_1 = 27      #  P8.17
BATT_LED_2 = 65      #  P8.18
BATT_LED_2_BLUE = 11 #  different on BB Blue
BATT_LED_3 = 61      #  P8.26
BATT_LED_4 = 26      #  P8.14

DEBOUNCE_INTERVAL = 0.5

import io, threading, time, os
import select

class InputTimeout(Exception):
    pass

class GPIO:

    def __init__(self, chip, line):
        self.chip = gpiod.Chip('gpiochip{}'.format(chip))
        self.line = self.chip.get_line(line)

    def request(self, type):
        self.line.request(consumer=str(id(self)), type=type)

    def release(self):
        self.line.release()
        
class Output(GPIO):
            
    def __init__(self, chip, line):

        # call super
        super().__init__(chip, line)
        self.request(type=gpiod.LINE_REQ_DIR_OUT)

    def set(self, state):
        return self.line.set_value(state)
    
class Input(GPIO):

    def __init__(self, chip, line):

        # call super
        super().__init__(chip, line)
        self.request(type=gpiod.LINE_REQ_DIR_IN)

    def read(self, timeout = None, pipe = None):

        # create pipe if necessary
        destroy_pipe = False
        if pipe is None:
            pipe = rcpy.create_pipe()
            destroy_pipe = True

        # request both edges and get file descriptor
        self.release()
        self.request(type=gpiod.LINE_REQ_EV_BOTH_EDGES)
        fdescriptor = self.line.event_get_fd()

        try:

            with os.fdopen(fdescriptor, 'rb', buffering = 0) as f:

                # create poller
                poller = select.poll()
                poller.register(f,
                                select.POLLPRI | select.POLLIN | 
                                select.POLLHUP | select.POLLERR)

                # listen to state change as well
                state_r_fd, state_w_fd = pipe
                poller.register(state_r_fd,
                                select.POLLIN |
                                select.POLLHUP | select.POLLERR)

                while rcpy.get_state() != rcpy.EXITING:

                    # wait for events
                    if timeout:
                        # can fail if timeout is given
                        events = poller.poll(timeout)
                        if len(events) == 0:
                            raise InputTimeout('Input did not change in more than {} ms'.format(timeout))

                    else:
                        # timeout = None, never fails
                        events = poller.poll()

                    # check flags
                    for fd, flag in events:

                        # state change
                        if fd is state_r_fd:
                            # get state
                            state = int(os.read(state_r_fd, 1))
                            if state == rcpy.EXITING:
                                # exit!
                                return

                        # input event
                        if fd == f.fileno():

                            # read event
                            event = self.line.event_read()

                            # Handle inputs
                            if flag & (select.POLLIN | select.POLLPRI):
                                # release line
                                self.release()
                                self.request(type=gpiod.LINE_REQ_DIR_IN)
                                # return read value
                                return self.get()

                            elif flag & (select.POLLHUP | select.POLLERR):
                                # raise exception
                                raise Exception('Could not read input {}'.format(self))

        finally:

            # release line
            self.release()
            self.request(type=gpiod.LINE_REQ_DIR_IN)

            # destroy pipe
            if destroy_pipe:
                rcpy.destroy_pipe(pipe)
            
    def get(self):
        return self.line.get_value()
        
    def is_high(self):
        return self.get() == HIGH

    def is_low(self):
        return self.get() == LOW

    def high_or_low(self, debounce = 0, timeout = 0, pipe = None):

        # repeat until event is detected
        while rcpy.get_state() != rcpy.EXITING:

            # read event
            value = self.read(timeout, pipe)
            
            # debounce
            k = 0
            current_value = value
            while k < debounce and value == current_value:
                time.sleep(DEBOUNCE_INTERVAL/1000)
                current_value = self.get()
                k += 1

            # check value
            if value == current_value:

                # return value
                return value

    def high(self, debounce = 0, timeout = 0, pipe = None):
        event = self.high_or_low(debounce, timeout, pipe)
        if event == HIGH:
            return True
        else:
            return False

    def low(self, debounce = 0, timeout = 0, pipe = None):
        event = self.high_or_low(debounce, timeout, pipe)
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

