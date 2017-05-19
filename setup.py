from setuptools import setup, Extension, find_packages
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

led = Extension("rcpy.led",
                sources = ["src/_led.c"],
                libraries = LIBS)

_buttons = Extension("rcpy._buttons",
                     sources = ["src/_buttons.c"],
                     libraries = LIBS)

setup(
    
    name="rcpy",
    version="0.2a",
    packages=find_packages(),

    # extensions
    ext_modules=[rcpy, mpu9250, encoder, gpio, motor, led,
                 _buttons],
    
    # metadata
    author="Mauricio C. de Oliveira",
    author_email="mauricio@ucsd.edu",
    description="Python interface for Robotics Cape",
    license="MIT",
    keywords="Robotics Cape beaglebone black",
    url="https://github.com/mcdeoliveira/rcpy"
    
)
