#!/usr/bin/env python3
# import python libraries
import time
import getopt, sys

# import rcpy library
# This automatically initizalizes the robotics cape
import rcpy 
import rcpy.mpu9250 as mpu9250

def usage():
    print("""usage: python rcpy_test_dmp [options] ...
Options are:
-m          enable magnetometer
-s rate     Set sample rate in HZ (default 100)
            Sample rate must be a divisor of 200
-c          Print compass angle
-a          Print accelerometer data
-g          Print gyro data
-t          Print Tait-Bryan angles
-q          Print quaternion vector
-f          Print fused data
-n          Newline (default = '\r')
-o          Show a menu to select IMU orientation
-h          print this help message""")

def main():

    # exit if no options
    if len(sys.argv) < 2:
        usage()
        sys.exit(2)

    # Parse command line
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hmpcagtqfos:", ["help"])

    except getopt.GetoptError as err:
        # print help information and exit:
        print('rcpy_test_dmp: illegal option {}'.format(sys.argv[1:]))
        usage()
        sys.exit(2)

    # defaults
    enable_magnetometer = False
    show_compass = False
    show_gyro = False
    show_accel = False
    show_quat = False
    show_tb = False
    sample_rate = 100
    enable_fusion = False
    show_period = False
    newline = '\r'

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in "-s":
            sample_rate = int(a)
        elif o == "-m":
            enable_magnetometer = True
        elif o == "-c":
            show_compass = True
        elif o == "-a":
            show_accel = True
        elif o == "-g":
            show_gyro = True
        elif o == "-q":
            show_quat = True
        elif o == "-t":
            show_tb = True
        elif o == "-f":
            enable_fusion = True
        elif o == "-p":
            show_period = True
        elif o == "-n":
            newline = a
        else:
            assert False, "Unhandled option"

    if show_compass and not enable_magnetometer:
        print('rcpy_test_dmp: -c can only be used with -m ')
        usage()
        sys.exit(2)
            
    # set state to rcpy.RUNNING
    rcpy.set_state(rcpy.RUNNING)

    # magnetometer ?
    mpu9250.initialize(enable_dmp=True,
                       dmp_sample_rate=sample_rate,
                       enable_fusion=enable_fusion,
                       enable_magnetometer=enable_magnetometer)

    # message
    print("Press Ctrl-C to exit")

    # header
    if show_accel:
        print("   Accel XYZ (m/s^2) |", end='')
    if show_gyro:
        print("    Gyro XYZ (deg/s) |", end='')
    if show_compass:
        print("     Mag Field XYZ (uT) |", end='')
        print("Head(rad)|", end='')
    if show_quat:
        print("                 Quaternion |", end='')
    if show_tb:
        print("    Tait Bryan (rad) |", end='')
    if show_period:
        print(" Ts (ms)", end='')
    print()
        
    try:

        # keep running
        while True:

            # running
            if rcpy.get_state() == rcpy.RUNNING:
                
                t0 = time.perf_counter()
                data = mpu9250.read()
                t1 = time.perf_counter()
                dt = t1 - t0
                t0 = t1

                print(newline, end='')
                if show_accel:
                    print('{0[0]:6.2f} {0[1]:6.2f} {0[2]:6.2f} |'
                          .format(data['accel']), end='')
                if show_gyro:
                    print('{0[0]:6.1f} {0[1]:6.1f} {0[2]:6.1f} |'
                          .format(data['gyro']), end='')
                if show_compass:
                    print('{0[0]:7.1f} {0[1]:7.1f} {0[2]:7.1f} |'
                          .format(data['mag']), end='')
                    print('  {:6.2f} |'
                          .format(data['head']), end='')
                if show_quat:
                    print('{0[0]:6.1f} {0[1]:6.1f} {0[2]:6.1f} {0[3]:6.1f} |'
                          .format(data['quat']), end='')
                if show_tb:
                    print('{0[0]:6.2f} {0[1]:6.2f} {0[2]:6.2f} |'
                          .format(data['tb']), end='')
                if show_period:
                    print(' {:7.2f}'.format(1000*dt), end='')
                        
                # no need to sleep

    except KeyboardInterrupt:
        # Catch Ctrl-C
        pass
    
    finally:

        # say bye
        print("\nBye Beaglebone!")
            
# exiting program will automatically clean up cape

if __name__ == "__main__":
    main()
