#!/usr/bin/env python3
# import python libraries
import time

# import rcpy library
# This automatically initizalizes the robotics cape
import rcpy 
import rcpy.mpu9250 as mpu9250

# welcome message
print("Hello BeagleBone!")
print("Press Ctrl-C to exit")

# enable dmp
sample_rate = 4
imu = mpu9250.IMU(enable_dmp = True,
                  dmp_sample_rate = sample_rate)

# set state to rcpy.RUNNING
rcpy.set_state(rcpy.RUNNING)

# spinning wheel
i = 0
spin = '-\|/'

try:

    # keep running forever
    while True:

        # read to synchronize with imu
        data = imu.read()
        
        # running?
        if rcpy.get_state() == rcpy.RUNNING:

            # do things
            print('\r{}'.format(spin[i % len(spin)]), end='')
            i = i + 1

        # paused?
        elif rcpy.get_state() == rcpy.PAUSED:
            # do other things
            pass
    
        # there is no need to sleep

except KeyboardInterrupt:
    # Catch Ctrl-C
    pass

finally:

    # say bye
    print("\nBye Beaglebone!")
            
# exiting program will automatically clean up cape
