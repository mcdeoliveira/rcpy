if __name__ == "__main__":

    # This is only necessary if package has not been installed
    import sys
    sys.path.append('..')

# import Python libraries
import threading
    
# import rcpy libraries
import rcpy 
import rcpy.button as button
import rcpy.led as led

# welcome message
print("Hello BeagleBone!")
print("Green and red LEDs are flashing")
print("Press button <MODE> to change the blink rate")
print("Press button <PAUSE> to stop or restart blinking")
print("Hold button <PAUSE> for 1.5 s to exit")
  
# configure LEDs
rates = (1, 5, 10)
index = 0

red = led.blink(led.RED, rates[index % len(rates)])
green = led.blink(led.RED, rates[index % len(rates)])

# initialize state
red.set_state(led.ON)
green.set_state(led.OFF)

# set state to rcpy.RUNNING
rcpy.set_state(rcpy.RUNNING)

# function to step rate
def step():
    while rcpy.set_state(rcpy.RUNNING):
        if button.pressed(button.MODE):
            # increment rate
            index += 1
            red.set_rate(rates[index % len(rates)])
            green.set_rate(rates[index % len(rates)])

# run step function on a thread
step_thread = threading.Thread(target=step)
step_thread.start()

# start blinking
red.start()
green.start()
blinking = True

try:
    # wait for PAUSE button
    while rcpy.get_state() == rcpy.RUNNING:

        # this is a blocking call!
        if button.pressed(button.PAUSE):

            # this is a blocking call with a timeout!
            if button.released(button.PAUSE, 1.5):
                # released too soon!

                # toggle start
                if blinking:
                    # stop leds
                    red.stop()
                    green.stop()
                    blinking = False

                else:
                    # start leds
                    red.start()
                    green.start()
                    blinking = True

            else:
                # timeout or did not release
                # exit
                break

except KeyboardInterrupt:
    # Catch Ctrl-C
    pass
        
finally:

    # wait for step_thread to end
    step_thread.join()
    
    # say bye
    print("\nBye Beaglebone!")
            
