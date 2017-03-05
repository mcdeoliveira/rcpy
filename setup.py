from distutils.core import setup, Extension
import platform

LIBS = ['roboticscape']
if platform.system().lower() == 'linux':
    LIBS.append('rt')

rc = Extension("rc.rcpy",
               sources = ["src/_rcpy.c"],
               libraries = LIBS)

mpu9250 = Extension("rc.mpu9250",
                    sources = ["src/_mpu9250.c"],
                    libraries = LIBS)

encoder = Extension("rc.encoder",
                    sources = ["src/_encoder.c"],
                    libraries = LIBS)

gpio = Extension("rc.gpio",
                 sources = ["src/_gpio.c"],
                 libraries = LIBS)

motor = Extension("rc.motor",
                  sources = ["src/_motor.c"],
                  libraries = LIBS)

setup(
    ext_modules=[rc, mpu9250, encoder, gpio, motor]
)
