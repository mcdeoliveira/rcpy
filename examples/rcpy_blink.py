# import Python libraries
import threading
    
# import rcpy libraries
import rcpy 
import rcpy.button as button
import rcpy.led as led

# configure LEDs
rates = (1, 0.5, 0.1)
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
def mode_pressed(event, index, rates):
    print("<MODE> pressed, stepping blinking rate")
    # increment rate
    index += 1
    button.red.set_rate(rates[index % len(rates)])
    button.green.set_rate(rates[index % len(rates)])
        
mode_event = button.ButtonEvent(button.mode,
                                button.ButtonEvent.PRESSED,
                                target = mode_pressed,
                                vargs = (index, rates))
mode_event.start()

# welcome message
print("Green and red LEDs should be flashing")
print("Press button <MODE> to change the blink rate")
print("Press button <PAUSE> to stop or restart blinking")
print("Hold button <PAUSE> for 1.5 s to exit")

try:
    
    while rcpy.get_state() != rcpy.EXITING:

        print("Waiting for <PAUSE> button...")
        
        # this is a blocking call!
        if button.pause.pressed():

            # pause pressed
            print("<PAUSE> pressed")

            # # this is a blocking call with a timeout!
            # if button.released(button.PAUSE, 1.5):
            #     # released too soon!

            #     # toggle start
            #     if blinking:
            #         print("Stopped blinking")
            #         # stop leds
            #         red.stop()
            #         green.stop()
            #         blinking = False

            #     else:
            #         print("Started blinking")
            #         # start leds
            #         red = led.blink(led.RED, rates[index % len(rates)], led.ON)
            #         green = led.blink(led.RED, rates[index % len(rates)], led.OFF)
            #         blinking = True

            # else:
            #     # timeout or did not release
            #     print("<PAUSE> held, exiting...")
            #     # exit
            #     break

except KeyboardInterrupt:
    # Catch Ctrl-C
    pass
        
finally:

    print("Exiting...")

    # stop threads
    blink_red.stop()
    blink_green.stop()
    mode_event.stop()
    
    blink_red.join()
    blink_green.join()
    mode_event.join()
    
    # say bye
    print("\nBye Beaglebone!")
            
