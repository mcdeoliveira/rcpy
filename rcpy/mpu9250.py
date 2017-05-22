import rcpy
from rcpy._mpu9250 import *

ACCEL_FSR_2G = 0
ACCEL_FSR_4G = 1
ACCEL_FSR_8G = 2
ACCEL_FSR_16G = 3

GYRO_FSR_250DPS = 0 
GYRO_FSR_500DPS = 1
GYRO_FSR_1000DPS = 2
GYRO_FSR_2000DPS = 3

ACCEL_DLPF_OFF = 0
ACCEL_DLPF_184 = 1
ACCEL_DLPF_92 = 2
ACCEL_DLPF_41 = 3
ACCEL_DLPF_20 = 4
ACCEL_DLPF_10 = 5
ACCEL_DLPF_5 = 6

GYRO_DLPF_OFF = 0
GYRO_DLPF_184 = 1
GYRO_DLPF_92 = 2
GYRO_DLPF_41 = 3
GYRO_DLPF_20 = 4
GYRO_DLPF_10 = 5
GYRO_DLPF_5 = 6

ORIENTATION_Z_UP	= 136,
ORIENTATION_Z_DOWN	= 396,
ORIENTATION_X_UP	= 14,
ORIENTATION_X_DOWN	= 266,
ORIENTATION_Y_UP	= 112,
ORIENTATION_Y_DOWN	= 336,
ORIENTATION_X_FORWARD	= 133,
ORIENTATION_X_BACK	= 161

# Uses Alex Martelli's Borg for making MPU9250 a singleton

class IMU():

    _shared_state = {}

    def __init__(self, **kwargs):

        # Makes sure clock is a singleton
        self.__dict__ = self._shared_state
        
        # Do not initialize if already initialized
        if not self.__dict__ == {}:
            return self.set(**kwargs)

        # get defaults
        defaults = get()

        # accel_fsr
        self.accel_fsr = kwargs.pop('accel_fsr', defaults['accel_fsr'])

        # gyro_fsr
        self.gyro_fsr = kwargs.pop('gyro_fsr', defaults['gyro_fsr'])

        # accel_dlpf
        self.accel_dlpf = kwargs.pop('accel_dlpf', defaults['accel_dlpf'])

        # gyro_dlpf
        self.gyro_dlpf = kwargs.pop('gyro_dlpf', defaults['gyro_dlpf'])

        # enable_magnetometer 
        self.enable_magnetometer = kwargs.pop('enable_magnetometer',
                                              defaults['enable_magnetometer'])

        # orientation
        self.orientation = kwargs.pop('orientation', defaults['orientation'])

        # compass_time_constant
        self.compass_time_constant = kwargs.pop('compass_time_constant',
                                                defaults['compass_time_constant'])

        # dmp_interrupt_priority
        self.dmp_interrupt_priority = kwargs.pop('dmp_interrupt_priority',
                                                 defaults['dmp_interrupt_priority'])
        
        # dmp_sample_rate
        self.dmp_sample_rate = kwargs.pop('dmp_sample_rate',
                                          defaults['dmp_sample_rate'])
        
        # show_warnings
        self.show_warnings = kwargs.pop('show_warnings',
                                        defaults['show_warnings'])
        
        # enable_dmp 
        self.enable_dmp = kwargs.pop('enable_dmp',
                                     True)
        
        # enable_fusion 
        self.enable_fusion = kwargs.pop('enable_fusion',
                                        defaults['enable_fusion'])

        # call mpu9250 initialize
        initialize(accel_fsr = self.accel_fsr,
                   gyro_fsr = self.gyro_fsr,
                   accel_dlpf = self.accel_dlpf,
                   gyro_dlpf = self.gyro_dlpf,
                   enable_magnetometer = self.enable_magnetometer,
                   orientation = self.orientation,
                   compass_time_constant = self.compass_time_constant,
                   dmp_interrupt_priority = self.dmp_interrupt_priority,
                   dmp_sample_rate = self.dmp_sample_rate,
                   show_warnings = self.show_warnings,
                   enable_dmp = self.enable_dmp,
                   enable_fusion = self.enable_fusion)

        # initialize data
        self.data = {}
                                          
    def set(self, **kwargs):

        # accel_fsr
        if 'accel_fsr' in kwargs:
            self.accel_fsr = kwargs.pop('accel_fsr')

        # gyro_fsr
        if 'gyro_fsr' in kwargs:
            self.gyro_fsr = kwargs.pop('gyro_fsr')

        # accel_dlpf
        if 'accel_dlpf' in kwargs:
            self.accel_dlpf = kwargs.pop('accel_dlpf')

        # gyro_dlpf
        if 'gyro_dlpf' in kwargs:
            self.gyro_dlpf = kwargs.pop('gyro_dlpf')

        # enable_magnetometer 
        if 'enable_magnetometer' in kwargs:
            self.enable_magnetometer = kwargs.pop('enable_magnetometer')

        # orientation
        if 'orientation' in kwargs:
            self.orientation = kwargs.pop('orientation')

        # compass_time_constant
        if 'compass_time_constant' in kwargs:
            self.compass_time_constant = kwargs.pop('compass_time_constant')

        # dmp_interrupt_priority
        if 'dmp_interrupt_priority' in kwargs:
            self.dmp_interrupt_priority = kwargs.pop('dmp_interrupt_priority')
        
        # dmp_sample_rate
        if 'dmp_sample_rate' in kwargs:
            self.dmp_sample_rate = kwargs.pop('dmp_sample_rate')
        
        # show_warnings
        if 'show_warnings' in kwargs:
            self.show_warnings = kwargs.pop('show_warnings')
        
        # enable_dmp 
        if 'enable_dmp' in kwargs:
            self.enable_dmp = kwargs.pop('enable_dmp')
        
        # enable_fusion 
        if 'enable_fusion' in kwargs:
            self.enable_fusion = kwargs.pop('enable_fusion')

        # call mpu9250 initialize
        initialize(accel_fsr = self.accel_fsr,
                   gyro_fsr = self.gyro_fsr,
                   accel_dlpf = self.accel_dlpf,
                   gyro_dlpf = self.gyro_dlpf,
                   enable_magnetometer = self.enable_magnetometer,
                   orientation = self.orientation,
                   compass_time_constant = self.compass_time_constant,
                   dmp_interrupt_priority = self.dmp_interrupt_priority,
                   dmp_sample_rate = self.dmp_sample_rate,
                   show_warnings = self.show_warnings,
                   enable_dmp = self.enable_dmp,
                   enable_fusion = self.enable_fusion)
    
    def read(self):

        # read mpu9250
        return read()
