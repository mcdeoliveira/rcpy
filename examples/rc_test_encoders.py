if __name__ == "__main__":

    # This is only necessary if package has not been installed
    import sys
    sys.path.append('..')

# import python libraries
import time
import getopt

# import rc library
# This automatically initizalizes the robotics cape
import rc 
import rc.encoder as encoder

def usage():
    print("""usage: python rc_test_encoders [options] ...
Options are:
-e encoder  specify a single encoder from 1-4, 0 for all motors
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
        print('rc_test_encoders: illegal option {}'.format(sys.argv[1:]))
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

    try:

        # set state to rc.RUNNING
        rc.set_state(rc.RUNNING);

        # message
        print("Press Ctrl-C to exit");

        # header
        if channel == 0:
            print('     E1 |     E2 |     E3 |     E4')
        else:
            print('     E{}'.format(channel))

        # keep running
        while rc.get_state() != rc.EXITING:

            # running
            if rc.get_state() == rc.RUNNING:

                if channel == 0:

                    # read all encoders
                    e1 = encoder.read(1)
                    e2 = encoder.read(2)
                    e3 = encoder.read(3)
                    e4 = encoder.read(4)

                    print('\r {:+6d} | {:+6d} | {:+6d} | {:+6d}'.format(e1,e2,e3,e4), end='')

                else:

                    # read one encoder
                    e = encoder.read(channel)

                    print('\r {:+6d}'.format(e), end='')
                        
            # sleep some
            time.sleep(.5)

    except (KeyboardInterrupt, SystemExit):
        # handle what to do when Ctrl-C was pressed
        pass
        
    finally:

        # say bye
        print("\nInterrupted.");
            
# exiting program will automatically clean up cape

if __name__ == "__main__":
    main()
