if __name__ == "__main__":

    # This is only necessary if package has not been installed
    import sys
    sys.path.append('..')

# import python libraries
import time

# import rcpy library
# This automatically initizalizes the robotics cape
import rcpy 

# welcome message
print("Hello BeagleBone!")
print("Press Ctrl-C to exit")
    
# set state to rcpy.RUNNING
rcpy.set_state(rcpy.RUNNING)

try:
    
    # keep running forever
    while True:

        # running?
        if rcpy.get_state() == rcpy.RUNNING:
            # do things
            pass
    
        # paused?
        elif rcpy.get_state() == rcpy.PAUSED:
            # do other things
            pass
    
        # sleep some
        time.sleep(1)

except KeyboardInterrupt:
    # Catch Ctrl-C
    pass
        
finally:

    # say bye
    print("\nBye Beaglebone!")
            
# exiting program will automatically clean up cape
