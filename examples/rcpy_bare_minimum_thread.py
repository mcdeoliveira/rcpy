#!/usr/bin/env python3
# import python libraries
import time
import threading

# import rcpy library
# This automatically initizalizes the robotics cape
import rcpy 
import rcpy.mpu9250 as mpu9250

# function to run on a thread
def thread_function(imu, name):

    # make sure the thread will terminate
    while rcpy.get_state() != rcpy.EXITING:

        # read to synchronize with imu
        data = imu.read()
        
        # handle other states
        if rcpy.get_state() == rcpy.RUNNING:

            # do things
            print('Hi from thread {}!'.format(name))
    
        # there is no need to sleep

# welcome message
print("Hello BeagleBone!")
print("Press Ctrl-C to exit")

# enable dmp
sample_rate = 8
imu = mpu9250.IMU(enable_dmp = True,
                  dmp_sample_rate = sample_rate)

# set state to rcpy.RUNNING
rcpy.set_state(rcpy.RUNNING)

# fire up threads
threads = []
threads.append(threading.Thread(target = thread_function, args = (imu, "#1")))
threads.append(threading.Thread(target = thread_function, args = (imu, "#2")))
for t in threads:
    t.start()

# go do other things
try:

    # keep running forever
    while True:

        # print some
        print('Hi from main loop!')
        
        # sleep some
        time.sleep(1)
        
except KeyboardInterrupt:
    # Catch Ctrl-C
    pass

finally:

    # wait for threads to finish
    for t in threads:
        t.join()
    
    # say bye
    print("\nBye Beaglebone!")
            
# exiting program will automatically clean up cape
