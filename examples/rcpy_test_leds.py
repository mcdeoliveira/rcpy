#!/usr/bin/env python3
# import rcpy libraries
import rcpy
import rcpy.led as led
import time

ON = 1
OFF = 0

# blink leds
green = led.LED(0,ON)
red = led.LED(1,OFF)


# set state to rcpy.RUNNING
rcpy.set_state(rcpy.RUNNING)



# welcome message
print("Green and red LEDs should be flashing")


try:

    # keep running
    while True:
        red.toggle()
        green.toggle()
        # sleep some
        time.sleep(.5)

except KeyboardInterrupt:
    # Catch Ctrl-C
    pass


finally:

    print("Exiting...")
    red.off()
    green.off()

    # say bye
    print("\nBye Beaglebone!")

