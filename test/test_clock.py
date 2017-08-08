import pytest

import rcpy.clock as clock
import time

def test1():

    class MyAction(clock.Action):

        def __init__(self):
            self.count = 0
        
        def run(self):
            self.count += 1

    action = MyAction()            
    obj = clock.Clock(action)

    obj.start()
    assert action.count == 0

    time.sleep(1.1*obj.period)
    assert action.count == 1
    
    time.sleep(1.1*obj.period)
    assert action.count == 2

    obj.toggle()
    
    time.sleep(1.1*obj.period)
    assert action.count == 2

    obj.toggle()
    
    time.sleep(1.1*obj.period)
    assert action.count == 3

    obj.stop()
    
if __name__ == '__main__':

    test1()
