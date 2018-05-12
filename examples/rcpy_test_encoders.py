#!/usr/bin/env python3
# import python libraries
import time
import getopt, sys

# import rcpy library
# This automatically initizalizes the robotics cape
import rcpy
import rcpy.encoder as encoder

def usage():
    print("""usage: python rcpy_test_encoders [options] ...
Options are:
-e encoder  specify a single encoder from 1-4, 0 for all channels
-h          print this help message""")

def main():

    # exit if no options
    if len(sys.argv) < 2:
        usage()
        sys.exit(2)

    # Parse command line
    try:
        opts, args = getopt.getopt(sys.argv[1:], "he:", ["help"])

    except getopt.GetoptError as err:
        # print help information and exit:
        print('rcpy_test_encoders: illegal option {}'.format(sys.argv[1:]))
        usage()
        sys.exit(2)

    # defaults
    channel = 0

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in "-e":
            channel = int(a)
        else:
            assert False, "Unhandled option"

    # set state to rcpy.RUNNING
    rcpy.set_state(rcpy.RUNNING)

    # message
    print("Press Ctrl-C to exit")

    # header
    if channel == 0:
        print('     E1 |     E2 |     E3 |     E4')
    else:
        print('     E{}'.format(channel))

    try:

        # keep running
        while True:

            # running
            if rcpy.get_state() == rcpy.RUNNING:

                if channel == 0:

                    # read all encoders
                    e1 = encoder.get(1)
                    e2 = encoder.get(2)
                    e3 = encoder.get(3)
                    e4 = encoder.get(4)

                    print('\r {:+6d} | {:+6d} | {:+6d} | {:+6d}'.format(e1,e2,e3,e4), end='')

                else:

                    # read one encoder
                    e = encoder.get(channel)

                    print('\r {:+6d}'.format(e), end='')

            # sleep some
            time.sleep(.5)

    except KeyboardInterrupt:
        # Catch Ctrl-C
        pass

    finally:

        # say bye
        print("\nBye Beaglebone!")

# exiting program will automatically clean up cape

if __name__ == "__main__":
    main()
