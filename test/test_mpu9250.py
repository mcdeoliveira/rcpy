import pytest

import time
import rc.mpu9250 as mpu9250

def interrupt(*vargs, **kwargs):

    print("HI!")

def test1():

    N = 1
    
    try:

        # no magnetometer
        mpu9250.initialize_imu(enable_magnetometer = False)
        
        print('\n   Accel XYZ(m/s^2)  |   Gyro XYZ (rad/s)  |   Temp (C)')

        for i in range(N):

            (ax,ay,az) = mpu9250.read_accel_data()
            (gx,gy,gz) = mpu9250.read_gyro_data()
            temp = mpu9250.read_imu_temp()

            print(('\r{:6.2f} {:6.2f} {:6.2f} |' +
                   '{:6.1f} {:6.1f} {:6.1f} | {:6.1f}').format(ax, ay, az,
                                                               gx, gy, gz, temp),
                  end='')

            time.sleep(1)

        with pytest.raises(mpu9250.error):
            mpu9250.read_mag_data()

        # consolidated read function
            
        for i in range(N):

            data = mpu9250.read()
            (ax, ay, az) = data['accel']
            (gx, gy, gz) = data['gyro']
            
            print(('\r{:6.2f} {:6.2f} {:6.2f} |' +
                   '{:6.1f} {:6.1f} {:6.1f} | {:6.1f}').format(ax, ay, az,
                                                               gx, gy, gz,
                                                               data['temp']),
                  end='')

            time.sleep(1)

        # with magnetometer
        mpu9250.initialize_imu(enable_magnetometer = True)
            
        print('\n   Accel XYZ(m/s^2)  |   Gyro XYZ (rad/s)  |  Mag Field XYZ(uT)  | Temp (C)')

        for i in range(N):

            (ax,ay,az) = mpu9250.read_accel_data()
            (gx,gy,gz) = mpu9250.read_gyro_data()
            (mx,my,mz) = mpu9250.read_mag_data()
            temp = mpu9250.read_imu_temp()

            print(('\r{:6.2f} {:6.2f} {:6.2f} |' +
                   '{:6.1f} {:6.1f} {:6.1f} |'
                   '{:6.1f} {:6.1f} {:6.1f} | {:6.1f}').format(ax, ay, az,
                                                               gx, gy, gz,
                                                               mx, my, mz, temp),
                  end='')

            time.sleep(1)

        # consolidated read function
            
        for i in range(N):

            data = mpu9250.read()
            (ax, ay, az) = data['accel']
            (gx, gy, gz) = data['gyro']
            (mx, my, mz) = data['mag']
            
            print(('\r{:6.2f} {:6.2f} {:6.2f} |' +
                   '{:6.1f} {:6.1f} {:6.1f} |'
                   '{:6.1f} {:6.1f} {:6.1f} | {:6.1f}').format(ax, ay, az,
                                                               gx, gy, gz,
                                                               mx, my, mz,
                                                               data['temp']),
                  end='')

            time.sleep(1)

    except (KeyboardInterrupt, SystemExit):
        pass

    finally:
        mpu9250.power_off_imu()

def test2():

    N = 200
    
    try:

        # with dmp, no magnetometer
        mpu9250.initialize_imu(enable_magnetometer = False, enable_dmp = True)
        
        print('\n   Accel XYZ(m/s^2)  |   Gyro XYZ (rad/s)  |   Temp (C)')

        for i in range(N):

            data = mpu9250.read()
            (ax, ay, az) = data['accel']
            (gx, gy, gz) = data['gyro']
            
            print(('\r{:6.2f} {:6.2f} {:6.2f} |' +
                   '{:6.1f} {:6.1f} {:6.1f} | {:6.1f}').format(ax, ay, az,
                                                               gx, gy, gz,
                                                               data['temp']),
                  end='')

        # with dmp, with magnetometer
        mpu9250.initialize_imu(enable_magnetometer = True, enable_dmp = True)
            
        print('\n   Accel XYZ(m/s^2)  |   Gyro XYZ (rad/s)  |  Mag Field XYZ(uT)  | Temp (C)')

        for i in range(N):

            data = mpu9250.read()
            (ax, ay, az) = data['accel']
            (gx, gy, gz) = data['gyro']
            (mx, my, mz) = data['mag']
            
            print(('\r{:6.2f} {:6.2f} {:6.2f} |' +
                   '{:6.1f} {:6.1f} {:6.1f} |'
                   '{:6.1f} {:6.1f} {:6.1f} | {:6.1f}').format(ax, ay, az,
                                                               gx, gy, gz,
                                                               mx, my, mz,
                                                               data['temp']),
                  end='')

    except (KeyboardInterrupt, SystemExit):
        pass

    finally:
        mpu9250.power_off_imu()
        
if __name__ == '__main__':

    test1()
    test2()
