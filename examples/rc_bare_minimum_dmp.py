if __name__ == "__main__":

    # This is only necessary if package has not been installed
    import sys
    sys.path.append('..')

# import python libraries
import time

# import rc library
# This automatically initizalizes the robotics cape
import rc 
import rc.mpu9250 as mpu9250 

try:

    # welcome message
    print("Hello BeagleBone!")
    print("Press Ctrl-C to exit")

    # enable dmp
    sample_rate = 4
    mpu9250.initialize(enable_dmp = True,
                       dmp_sample_rate = sample_rate)
    
    # set state to rc.RUNNING
    rc.set_state(rc.RUNNING)

    # keep running until state changes to rc.EXITING
    i = 0
    spin = '-\|/'
    while rc.get_state() != rc.EXITING:

        # read to synchronize with imu
        data = mpu9250.read()
        
        # handle other states
        if rc.get_state() == rc.RUNNING:

            # do things
            print('\r{}'.format(spin[i % len(spin)]), end='')
            i = i + 1
    
        elif rc.get_state() == rc.PAUSED:
            # do other things
            pass
    
        # there is no need to sleep

except (KeyboardInterrupt, SystemExit):
    # handle what to do when Ctrl-C was pressed
    pass
        
finally:

    # say bye
    print("\nBye Beaglebone!")
            
# exiting program will automatically clean up cape
