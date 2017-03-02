from distutils.core import setup, Extension
import platform

MPU9250_LIBS = ['roboticscape']
if platform.system().lower() == 'linux':
    MPU9250_LIBS.append('rt')

mpu9250 = Extension("rc.mpu9250",
                    sources = ["src/_mpu9250.c"],
                    libraries = MPU9250_LIBS)

setup(
      ext_modules=[mpu9250]
)
