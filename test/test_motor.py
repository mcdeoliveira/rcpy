import pytest

import time
import rcpy.motor as motor

def test1():

    N = 5

    try:
        
        # enable
        motor.enable()
        time.sleep(.5)

        # disable
        motor.disable()
        time.sleep(.5)

        # enable again
        motor.enable()

        # spin motor 2 forward and back
        motor.set(2, 1)
        time.sleep(2)

        motor.set_free_spin(2)
        time.sleep(1)

        motor.set(2, -1)
        time.sleep(2)

        motor.set_free_spin(2)

        # spin motor 2 forward and back
        motor.set(3, 1)
        time.sleep(2)
    
        motor.set_free_spin(3)
        time.sleep(3)

        motor.set(3, -1)
        time.sleep(2)

        motor.set_free_spin(3)

        # disable motor
        motor.disable()

    except (KeyboardInterrupt, SystemExit):
        pass
        
    finally:

        motor.disable()
    
    
if __name__ == '__main__':

    test1()
