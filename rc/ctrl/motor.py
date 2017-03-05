import warnings
import time

if __name__ == "__main__":

    import sys
    sys.path.append('.')
    sys.path.append('/root/beaglebone/python')

import ctrl.block as block

import rc
import rc.motor as mtr

# enable motor
mtr.enable()

# make sure it is disabled when destroyed
import atexit; atexit.register(mtr.disable)

class Motor(block.Block):
        
    def __init__(self, *vars, **kwargs):

        self.motor = kwargs.pop('motor', 2)

        # call super
        super().__init__(*vars, **kwargs)

        mtr.set(self.motor, 0)
        mtr.free_spin(self.motor)

    def set_enabled(self, enabled = True):

        # call super
        super().set_enabled(enabled)

        if not enabled:

            # write 0 to motor
            mtr.set(self.motor, 0)
            mtr.free_spin(self.motor)

    def write(self, *values):

        #print('> write to motor')
        if self.enabled:

            mtr.set(self.motor, values[0]/100)

if __name__ == "__main__":

    import time, math

    print("> Testing Motor1")
    
    motor1 = Motor(motor = 2)

    # run motor forward
    motor1.write(100)
    time.sleep(1)

    # stop motor
    motor1.write(0)
    time.sleep(1)

    # run back
    motor1.write(-100)
    time.sleep(1)

    # stop motor
    motor1.write(0)

    print("> Testing Motor2")

    motor2 = Motor(motor = 3)

    # run motor forward
    motor2.write(100)
    time.sleep(1)

    # stop motor
    motor2.write(0)
    time.sleep(1)

    # run back
    motor2.write(-100)
    time.sleep(1)

    # stop motor
    motor2.write(0)
