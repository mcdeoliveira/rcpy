import pytest

import time
import rcpy.encoder as encoder

def test1():

    N = 5
    
    # set to 10
    
    encoder.set(1, 10)
    assert encoder.read(1) == 10

    encoder.set(2, 10)
    assert encoder.read(2) == 10
    
    encoder.set(3, 10)
    assert encoder.read(3) == 10
    
    encoder.set(4, 10)
    assert encoder.read(4) == 10

    # default to zero
    
    encoder.set(1)
    assert encoder.read(1) == 0

    encoder.set(2)
    assert encoder.read(2) == 0
    
    encoder.set(3)
    assert encoder.read(3) == 0
    
    encoder.set(4)
    assert encoder.read(4) == 0
    
    print('\n ENC #1 |  ENC #2 |  ENC #3 |  ENC #4')

    for i in range(N):

        e1 = encoder.read(1)
        e2 = encoder.read(2)
        e3 = encoder.read(3)
        e4 = encoder.read(4)
        
        print('\r{:7d} | {:7d} | {:7d} | {:7d}'.format(e1,e2,e3,e4),
              end='')
        
        time.sleep(1)

if __name__ == '__main__':

    test1()
