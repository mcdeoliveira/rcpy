#!/usr/bin/env python3
# import python libraries
import time, math
import getopt, sys

# import rcpy library
# This automatically initizalizes the robotics cape
import rcpy 
import rcpy.motor as motor

def usage():
    print("""usage: python rcpy_test_motors [options] ...
Options are:
-d duty     define a duty cycle from -1.0 to 1.0
-m motor    specify a single motor from 1-4, 0 for all motors
-s          sweep motors back and forward at duty cycle
-b          enable motor brake function
-f          enable free spin function
-n          number of steps per sweep (default = 20)
-t          period of sweep (default = 4s)
-h          print this help message""")

def main():

    # exit if no options
    if len(sys.argv) < 2:
        usage()
        sys.exit(2)
    
    # Parse command line
    try:
        opts, args = getopt.getopt(sys.argv[1:], "bfhsd:m:", ["help"])

    except getopt.GetoptError as err:
        # print help information and exit:
        print('rcpy_test_motors: illegal option {}'.format(sys.argv[1:]))
        usage()
        sys.exit(2)

    # defaults
    duty = 0.0
    channel = 0
    sweep = False
    brk = False
    free = False
    steps = 20
    period = 4

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in "-d":
            duty = float(a)
        elif o in "-m":
            channel = int(a)
        elif o == "-s":
            sweep = True
        elif o == "-b":
            brk = True
        elif o == "-f":
            free = True
        elif o == "-t":
            period = float(a)
        elif o == "-n":
            steps = int(a)
        else:
            assert False, "Unhandled option"

    # set state to rcpy.RUNNING
    rcpy.set_state(rcpy.RUNNING)

    # set motor duty (only one option at a time)
    if brk:
        print('Breaking motor {}'.format(channel))
        motor.set_brake(channel)
        sweep = False
    elif free:
        print('Setting motor {} free'.format(channel))
        motor.set_free_spin(channel)
        sweep = False
    elif duty != 0:
        if not sweep:
            print('Setting motor {} to {} duty'.format(channel, duty))
            motor.set(channel, duty)
        else:
            print('Sweeping motor {} to {} duty'.format(channel, duty))
    else:
        sweep = False

    # message
    print("Press Ctrl-C to exit")
        
    try:

        # sweep
        if sweep:

            d = 0
            direction = 1
            duty = math.fabs(duty)
            delta = duty/steps
            dt = period/steps/2
            
            # keep running
            while rcpy.get_state() != rcpy.EXITING:

                # running
                if rcpy.get_state() == rcpy.RUNNING:

                    # increment duty
                    d = d + direction * delta
                    motor.set(channel, d)

                    # end of range?
                    if d > duty or d < -duty:
                        direction = direction * -1
                        
                elif rcpy.get_state() == rcpy.PAUSED:

                    # set motors to free spin
                    motor.set_free_spin(channel)
                    d = 0
                    
                # sleep some
                time.sleep(dt)

        # or do nothing
        else:

            # keep running
            while rcpy.get_state() != rcpy.EXITING:
                
                # sleep some
                time.sleep(1)
            
    except KeyboardInterrupt:
        # handle what to do when Ctrl-C was pressed
        pass
        
    finally:

        # say bye
        print("\nBye Beaglebone!")
            
# exiting program will automatically clean up cape

if __name__ == "__main__":
    main()
