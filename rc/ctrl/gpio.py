if __name__ == "__main__":

    import sys
    sys.path.append('.')
    sys.path.append('/root/beaglebone/python')

import ctrl.block as block

import rc.GPIO as GPIO

class Input(block.BufferBlock):

    def __init__(self,
                 pin = GPIO.PAUSE_BTN,
                 *vars, **kwargs):

        # set pin
        self.pin = pin

        # setup as input
        # GPIO.GPIO.set_dir(self.pin, GPIO.IN)

        # call super
        super().__init__(*vars, **kwargs)

    def read(self):

        #print('> read')
        if self.enabled:

            # read digital pin
            self.buffer = (GPIO.GPIO.get_value(self.pin), )
        
        return self.buffer

class Output(block.BufferBlock):

    def __init__(self,
                 pin = GPIO.RED_LED,
                 *vars, **kwargs):

        # set pin
        self.pin = pin

        # setup as output
        #GPIO.GPIO.set_dir(self.pin, GPIO.OUT)

        # call super
        super().__init__(*vars, **kwargs)

    def write(self, *values):

        #print('> read')
        if self.enabled:

            # write to digital pin
            GPIO.GPIO.set_value(self.pin, values[0])
        
if __name__ == "__main__":

    import time, math

    print("> Testing GPIO input")
    
    #input = Input(pin=GPIO.PAUSE_BTN)
    #(x,) = input.read()

    #print('> GPIO {} = {:5.3f}'.format(input.pin, x))
    
    print("> Testing GPIO output")
    
    output = Output(pin=GPIO.MDIR1A)

    for i in range(10):
        output.write(1)
        time.sleep(.5)
        output.write(0)
        time.sleep(.5)
