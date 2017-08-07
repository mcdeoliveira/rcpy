import pytest

import rcpy.clock as clock
import time

def test1():

    class MyClock(Clock):

        def __init__(self):
            self.count = 0
        
        def action(self):
            self.count += 1
    
    obj = clock.MyClock()

    obj.start()
    assert obj.count == 0

    time.sleep(self.period)
    assert obj.count == 1
    
    time.sleep(self.period)
    assert obj.count == 2

    obj.toggle()
    
    time.sleep(self.period)
    assert obj.count == 2

    obj.toggle()
    
    time.sleep(self.period)
    assert obj.count == 3

if __name__ == '__main__':

    test1()
