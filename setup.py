from setuptools import setup, Extension, find_packages
import platform

LIBS = ['roboticscape']
if platform.system().lower() == 'linux':
    LIBS.append('rt')

rcpy = Extension("rcpy.rcpy",
               sources = ["src/_rcpy.c"],
               libraries = LIBS)

_mpu9250 = Extension("rcpy._mpu9250",
                     sources = ["src/_mpu9250.c"],
                     libraries = LIBS)

_encoder = Extension("rcpy._encoder",
                     sources = ["src/_encoder.c"],
                     libraries = LIBS)

_gpio = Extension("rcpy._gpio",
                  sources = ["src/_gpio.c"],
                  libraries = LIBS)

_gpio_mmap = Extension("rcpy._gpio_mmap",
                       sources = ["src/_gpio_mmap.c"],
                       libraries = LIBS)

_motor = Extension("rcpy._motor",
                   sources = ["src/_motor.c"],
                   libraries = LIBS)

setup(
    
    name="rcpy",
    version="0.2a",
    packages=find_packages(),

    # extensions
    ext_modules=[rcpy,
                 _mpu9250,
                 _encoder, _motor,
                 _gpio, _gpio_mmap],
    
    # metadata
    author="Mauricio C. de Oliveira",
    author_email="mauricio@ucsd.edu",
    description="Python interface for Robotics Cape",
    license="MIT",
    keywords="Robotics Cape beaglebone black",
    url="https://github.com/mcdeoliveira/rcpy"
    
)
