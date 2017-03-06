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
import rc.mpu9250 as mpu9250

def usage():
    print("""usage: python rc_test_imu [options] ...
Options are:
-m          enable magnetometer
-h          print this help message""")

def main():

    # Parse command line
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hm", ["help"])

    except getopt.GetoptError as err:
        # print help information and exit:
        print('rc_test_imu: illegal option {}'.format(sys.argv[1:]))
        usage()
        sys.exit(2)

    # defaults
    enable_magnetometer = False

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o == "-m":
            enable_magnetometer = True
        else:
            assert False, "Unhandled option"

    try:

        # set state to rc.RUNNING
        rc.set_state(rc.RUNNING)

        # no magnetometer
        mpu9250.initialize(enable_magnetometer = enable_magnetometer)
        
        # message
        print("try 'python rc_test_imu -h' to see other options")
        print("Press Ctrl-C to exit")

        # header
        print("   Accel XYZ (m/s^2) |"
              "    Gyro XYZ (deg/s) |", end='')
        if enable_magnetometer:
            print("  Mag Field XYZ (uT) |", end='')
        print(' Temp (C)')

        # keep running
        while rc.get_state() != rc.EXITING:

            # running
            if rc.get_state() == rc.RUNNING:
                
                temp = mpu9250.read_imu_temp()
                data = mpu9250.read()
                
                if enable_magnetometer:
                    print(('\r{0[0]:6.2f} {0[1]:6.2f} {0[2]:6.2f} |'
                           '{1[0]:6.1f} {1[1]:6.1f} {1[2]:6.1f} |'
                           '{2[0]:6.1f} {2[1]:6.1f} {2[2]:6.1f} |'
                           '   {3:6.1f}').format(data['accel'],
                                                 data['gyro'],
                                                 data['mag'],
                                                 temp),
                          end='')
                else:
                    print(('\r{0[0]:6.2f} {0[1]:6.2f} {0[2]:6.2f} |'
                           '{1[0]:6.1f} {1[1]:6.1f} {1[2]:6.1f} |'
                           '   {2:6.1f}').format(data['accel'],
                                                 data['gyro'],
                                                 temp),
                          end='')
                        
            # sleep some
            time.sleep(.5)

    except (KeyboardInterrupt, SystemExit):
        # handle what to do when Ctrl-C was pressed
        pass
        
    finally:

        # say bye
        print("\nInterrupted.")
            
# exiting program will automatically clean up cape

if __name__ == "__main__":
    main()
