from distutils.core import setup, Extension
import platform

LIBS = ['roboticscape']
if platform.system().lower() == 'linux':
    LIBS.append('rt')

rcpy = Extension("rcpy.rcpy",
               sources = ["src/_rcpy.c"],
               libraries = LIBS)

mpu9250 = Extension("rcpy.mpu9250",
                    sources = ["src/_mpu9250.c"],
                    libraries = LIBS)

encoder = Extension("rcpy.encoder",
                    sources = ["src/_encoder.c"],
                    libraries = LIBS)

gpio = Extension("rcpy.gpio",
                 sources = ["src/_gpio.c"],
                 libraries = LIBS)

motor = Extension("rcpy.motor",
                  sources = ["src/_motor.c"],
                  libraries = LIBS)

setup(
    ext_modules=[rcpy, mpu9250, encoder, gpio, motor]
)
