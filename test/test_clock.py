import pytest

import rcpy.clock as clock
import time

def test1():

    class MyAction(clock.Action):

        def __init__(self):
            self.count = 0
        
        def run(self):
            self.count += 1
        
    obj = clock.MyClock(MyAction())

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
