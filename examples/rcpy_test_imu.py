#!/usr/bin/env python3
# import python libraries
import time
import getopt, sys

# import rcpy library
# This automatically initizalizes the robotics cape
import rcpy 
import rcpy.mpu9250 as mpu9250

def usage():
    print("""usage: python rcpy_test_imu [options] ...
Options are:
-m          enable magnetometer
-h          print this help message""")

def main():

    # Parse command line
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hm", ["help"])

    except getopt.GetoptError as err:
        # print help information and exit:
        print('rcpy_test_imu: illegal option {}'.format(sys.argv[1:]))
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

    # set state to rcpy.RUNNING
    rcpy.set_state(rcpy.RUNNING)

    # no magnetometer
    mpu9250.initialize(enable_magnetometer = enable_magnetometer)

    # message
    print("try 'python rcpy_test_imu -h' to see other options")
    print("Press Ctrl-C to exit")

    # header
    print("   Accel XYZ (m/s^2) |"
          "    Gyro XYZ (deg/s) |", end='')
    if enable_magnetometer:
        print("  Mag Field XYZ (uT) |", end='')
    print(' Temp (C)')

    try:

        # keep running
        while True:

            # running
            if rcpy.get_state() == rcpy.RUNNING:
                
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

    except KeyboardInterrupt:
        # Catch Ctrl-C
        pass
    
    finally:

        # say bye
        print("\nBye Beaglebone!")
            
# exiting program will automatically clean up cape

if __name__ == "__main__":
    main()
