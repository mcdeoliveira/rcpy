import warnings
import math
import struct
import itertools

if __name__ == "__main__":

    import sys
    sys.path.append('.')
    sys.path.append('/root/beaglebone/python')

import ctrl.block as block

from rc.ctrl import clock as clk

class Raw(block.BufferBlock):
        
    def __init__(self, 
                 clock = clk.Clock(), # is a singleton
                 *vars, **kwargs):

        # make sure clock is Clock
        assert isinstance(clock, clk.Clock)
        self.clock = clock

        # call super
        super().__init__(*vars, **kwargs)

    def read(self):

        #print('> read')
        if self.enabled:

            # read imu
            data = self.clock.get_imu()

            # units (m/s^2) and (rad/s)
            self.buffer = itertools.chain(data['accel'],
                                          data['gyro'])
        
        #print('< read')
        return self.buffer

class Inclinometer(Raw):

    def __init__(self, *vars, **kwargs):

        # turns initialization
        self.turns = 0
        self.theta = 0
        self.threshold = 0.25

        # call super
        super().__init__(*vars, **kwargs)

    def reset(self):

        self.turns = 0
        
    def read(self):

        #print('> read')
        if self.enabled:

            # read imu
            data = self.clock.get_imu()
        
            # read IMU
            ax, ay, az = data['accel']
            gx, gy, gz = data['gyro']

            # compensate for turns
            theta = -math.atan2(az, ay) / (2 * math.pi)
            if (theta < 0 and self.theta > 0):
                if (self.theta - theta > self.threshold):
                    self.turns += 1
            elif (theta > 0 and self.theta < 0):
                if (theta - self.theta > self.threshold):
                    self.turns -= 1
            self.theta = theta
                    
            self.buffer = (self.turns + theta, gx / 360)
        
        #print('< read')
        return self.buffer

if __name__ == "__main__":

    import time, math
    from time import perf_counter

    T = 0.04
    K = 1000

    print("\n> Testing Inclinometer")
    
    giro = Inclinometer()
    print("\n> ")
    giro.set_enabled(enabled = True)

    N = 1000
    for k in range(N):
        
        # read inclinometer
        giro.clock.read()
        (theta, thetadot) = giro.read()

        print('\r> theta = {:+05.3f}  theta dot = {:+05.3f} 1/s'.format(theta, thetadot), end='')
