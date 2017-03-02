import pytest

import time
import rc.mpu9250 as mpu9250

def test1():

    try:

        print('   Accel XYZ(m/s^2)  |   Gyro XYZ (rad/s)  |  Mag Field XYZ(uT)  | Temp (C)')

        for i in range(60):

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

    except (KeyboardInterrupt, SystemExit):
        pass

    finally:
        mpu9250.power_off_imu()

if __name__ == '__main__':

    test1()
