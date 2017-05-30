#!/usr/bin/env python3
# import rcpy libraries
import rcpy 
import rcpy.gpio as gpio
import rcpy.button as button
import rcpy.led as led

# configure LEDs
rates = (0.5, 0.25, 0.1)
index = 0

# blink leds
led.red.on()
led.green.off()
blink_red = led.Blink(led.red, rates[index % len(rates)])
blink_green = led.Blink(led.green, rates[index % len(rates)])
blink_red.start()
blink_green.start()

# set state to rcpy.RUNNING
rcpy.set_state(rcpy.RUNNING)

# mode pressed?
def mode_pressed(input, event, blink_red, blink_green, rates):

    # increment rate
    global index
    index += 1
    
    print("<MODE> pressed, stepping blinking rate to {} s".format(rates[index % len(rates)]))

    # change blink period
    blink_red.set_period(rates[index % len(rates)])
    blink_green.set_period(rates[index % len(rates)])
    
    # reinitialize leds
    led.red.on()
    led.green.off()

# create and start ButtonEvent
mode_event = button.ButtonEvent(button.mode,
                                button.ButtonEvent.PRESSED,
                                target = mode_pressed,
                                vargs = (blink_red, blink_green, rates))
mode_event.start()

# welcome message
print("Green and red LEDs should be flashing")
print("Press button <MODE> to change the blink rate")
print("Press button <PAUSE> to stop or restart blinking")
print("Hold button <PAUSE> for 2 s to exit")

try:
    
    while rcpy.get_state() != rcpy.EXITING:

        # this is a blocking call!
        if button.pause.pressed():

            # pause pressed
            
            try:
            
                # this is a blocking call with a timeout!
                if button.pause.released(timeout = 2000):

                    # released too soon!
                    print("<PAUSE> pressed, toggle blinking")
                    
                    # toggle blinking
                    blink_red.toggle()
                    blink_green.toggle()

            except gpio.InputTimeout:
                
                # timeout 
                print("<PAUSE> held, exiting...")
                
                # exit
                rcpy.set_state(rcpy.EXITING)

except KeyboardInterrupt:
    # Catch Ctrl-C
    pass
        
finally:

    print("Exiting...")
    mode_event.stop()
    blink_red.stop()
    blink_green.stop()
    
    # say bye
    print("\nBye Beaglebone!")
            
