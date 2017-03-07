if __name__ == "__main__":

    # This is only necessary if package has not been installed
    import sys
    sys.path.append('..')

# import python libraries
import time
import threading

# import rc library
# This automatically initizalizes the robotics cape
import rc 
import rc.mpu9250 as mpu9250 

# function to run on a thread
def thread_function(name):

    # make sure the thread will terminate
    while rc.get_state() != rc.EXITING:

        # read to synchronize with imu
        data = mpu9250.read()
        
        # handle other states
        if rc.get_state() == rc.RUNNING:

            # do things
            print('Hi from thread {}!'.format(name))
    
        # there is no need to sleep

# welcome message
print("Hello BeagleBone!")
print("Press Ctrl-C to exit")

# enable dmp
sample_rate = 8
mpu9250.initialize(enable_dmp = True,
                   dmp_sample_rate = sample_rate)

# set state to rc.RUNNING
rc.set_state(rc.RUNNING)

# fire up threads
thread1 = threading.Thread(target = thread_function, args = ("#1",))
thread2 = threading.Thread(target = thread_function, args = ("#2",))
thread1.start()
thread2.start()

# go do other things until state changes to rc.EXITING
try:

    while rc.get_state() != rc.EXITING:

        # print some
        print('Hi from main loop!')
        
        # sleep some
        time.sleep(1)
        
finally:

    # say bye
    print("\nBye Beaglebone!")
            
# exiting program will automatically clean up cape