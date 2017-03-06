if __name__ == "__main__":

    # This is only necessary if package has not been installed
    import sys
    sys.path.append('..')

# import python libraries
import time

# import rc library
# This automatically initizalizes the robotics cape
import rc 

try:

    # welcome message
    print("Hello BeagleBone!")
    print("Press Ctrl-C to exit")
    
    # set state to rc.RUNNING
    rc.set_state(rc.RUNNING)

    # keep running until state changes to rc.EXITING
    while rc.get_state() != rc.EXITING:

        # handle other states
        if rc.get_state() == rc.RUNNING:
            # do things
            pass
    
        elif rc.get_state() == rc.PAUSED:
            # do other things
            pass
    
        # sleep some
        time.sleep(1)

except (KeyboardInterrupt, SystemExit):
    # handle what to do when Ctrl-C was pressed
    pass
        
finally:

    # say bye
    print("\nBye Beaglebone!")
            
# exiting program will automatically clean up cape
