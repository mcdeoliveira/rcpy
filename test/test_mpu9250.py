import pytest

import time
import rcpy.mpu9250 as mpu9250

def test1():

    N = 1
    
    try:

        # no magnetometer
        mpu9250.initialize(enable_magnetometer = False)

        conf = mpu9250.get()
        assert conf == {'orientation': 136, 'accel_dlpf': 2, 'gyro_dlpf': 2, 'compass_time_constant': 5.0, 'enable_fusion': False, 'enable_dmp': False, 'enable_magnetometer': False, 'accel_fsr': 1, 'dmp_sample_rate': 100, 'show_warnings': False, 'gyro_fsr': 2, 'dmp_interrupt_priority': 98}
        
        print('\n   Accel XYZ(m/s^2)  |   Gyro XYZ (rad/s)  |   Temp (C)')

        for i in range(N):

            (ax,ay,az) = mpu9250.read_accel_data()
            (gx,gy,gz) = mpu9250.read_gyro_data()
            temp = mpu9250.read_imu_temp()

            print(('\r{:6.2f} {:6.2f} {:6.2f} |' +
                   '{:6.1f} {:6.1f} {:6.1f} | {:6.1f}')
                  .format(ax, ay, az,
                          gx, gy, gz, temp),
                  end='')

            time.sleep(1)

        with pytest.raises(mpu9250.error):
            mpu9250.read_mag_data()

        # consolidated read function
            
        for i in range(N):

            data = mpu9250.read()
            print(('\r{0[0]:6.2f} {0[1]:6.2f} {0[2]:6.2f} |'
                   '{1[0]:6.1f} {1[1]:6.1f} {1[2]:6.1f} |')
                  .format(data['accel'],
                          data['gyro']),
                  end='')

            time.sleep(1)

        # with magnetometer
        mpu9250.initialize(enable_magnetometer = True)
            
        conf = mpu9250.get()
        assert conf == {'orientation': 136, 'accel_dlpf': 2, 'gyro_dlpf': 2, 'compass_time_constant': 5.0, 'enable_fusion': False, 'enable_dmp': False, 'enable_magnetometer': True, 'accel_fsr': 1, 'dmp_sample_rate': 100, 'show_warnings': False, 'gyro_fsr': 2, 'dmp_interrupt_priority': 98}
        
        print('\n   Accel XYZ(m/s^2)  |   Gyro XYZ (rad/s)  |  Mag Field XYZ(uT)  | Temp (C)')

        for i in range(N):

            (ax,ay,az) = mpu9250.read_accel_data()
            (gx,gy,gz) = mpu9250.read_gyro_data()
            (mx,my,mz) = mpu9250.read_mag_data()
            temp = mpu9250.read_imu_temp()

            print(('\r{:6.2f} {:6.2f} {:6.2f} |' +
                   '{:6.1f} {:6.1f} {:6.1f} |'
                   '{:6.1f} {:6.1f} {:6.1f} | {:6.1f}')
                  .format(ax, ay, az,
                          gx, gy, gz,
                          mx, my, mz, temp),
                  end='')

            time.sleep(1)

        # consolidated read function
            
        for i in range(N):

            data = mpu9250.read()
            print(('\r{0[0]:6.2f} {0[1]:6.2f} {0[2]:6.2f} |'
                   '{1[0]:6.1f} {1[1]:6.1f} {1[2]:6.1f} |'
                   '{2[0]:6.1f} {2[1]:6.1f} {2[2]:6.1f} |')
                  .format(data['accel'],
                          data['gyro'],
                          data['mag']),
                  end='')

            time.sleep(1)

    except (KeyboardInterrupt, SystemExit):
        pass

    finally:
        mpu9250.power_off()

def test2():

    N = 200
    
    try:

        # with dmp, no magnetometer
        mpu9250.initialize(enable_magnetometer = False, enable_dmp = True)
        
        conf = mpu9250.get()
        assert conf == {'orientation': 136, 'accel_dlpf': 2, 'gyro_dlpf': 2, 'compass_time_constant': 5.0, 'enable_fusion': False, 'enable_dmp': True, 'enable_magnetometer': False, 'accel_fsr': 1, 'dmp_sample_rate': 100, 'show_warnings': False, 'gyro_fsr': 2, 'dmp_interrupt_priority': 98}
        
        print('\n   Accel XYZ(m/s^2)  |   Gyro XYZ (rad/s)  |   Temp (C)')

        for i in range(N):

            data = mpu9250.read()
            print(('\r{0[0]:6.2f} {0[1]:6.2f} {0[2]:6.2f} |'
                   '{1[0]:6.1f} {1[1]:6.1f} {1[2]:6.1f} |')
                  .format(data['accel'],
                          data['gyro']),
                  end='')

        # with dmp, with magnetometer
        mpu9250.initialize(enable_magnetometer = True, enable_dmp = True)
            
        conf = mpu9250.get()
        assert conf == {'orientation': 136, 'accel_dlpf': 2, 'gyro_dlpf': 2, 'compass_time_constant': 5.0, 'enable_fusion': False, 'enable_dmp': True, 'enable_magnetometer': True, 'accel_fsr': 1, 'dmp_sample_rate': 100, 'show_warnings': False, 'gyro_fsr': 2, 'dmp_interrupt_priority': 98}
        
        print('\n   Accel XYZ(m/s^2)  |   Gyro XYZ (rad/s)  |  Mag Field XYZ(uT)  | Temp (C)')

        for i in range(N):

            data = mpu9250.read()
            print(('\r{0[0]:6.2f} {0[1]:6.2f} {0[2]:6.2f} |'
                   '{1[0]:6.1f} {1[1]:6.1f} {1[2]:6.1f} |'
                   '{2[0]:6.1f} {2[1]:6.1f} {2[2]:6.1f} |')
                  .format(data['accel'],
                          data['gyro'],
                          data['mag']),
                  end='')

    except (KeyboardInterrupt, SystemExit):
        pass

    finally:
        mpu9250.power_off()
        
if __name__ == '__main__':

    test1()
    test2()
