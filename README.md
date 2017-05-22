# rcpy: Python 3 Interface for the Robotics Cape on the Beaglebone Black and the Beaglebone Blue

**Release 0.2a**

This is a Python library with bindings for some of the functionality of the [Robotics Cape library](https://github.com/StrawsonDesign/Robotics_Cape_Installer).

We only support Python 3, and are not interested in Python 2 at all.

Not all functions are supported. Currently supported functions are:

1. MPU9250
2. PWM motors
3. Encoders
4. LEDs
5. Buttons
6. GPIO inputs

You might also be interested in the [ctrl package](https://github.com/mcdeoliveira/ctrl).

## Installation

As of today you will need a modified version of the current Robotics
Cape library. You can clone it from my fork:

    git clone https://github.com/mcdeoliveira/Robotics_Cape_Installer

Make sure you compile and install the modified version of the library:

    cd Robotics_Cape_Installer/libraries
    make clean
    make install

Clone this repository:

    git clone https://github.com/mcdeoliveira/rcpy

If you have not installed python3 yet type

    sudo apt install python3 python3-setuptools python3-dev

Finally run setup.py install:

    python3 setup.py install

## Available Documentation:

* [HTML](http://guitar.ucsd.edu/rcpy/html/index.html)

* [PDF](http://guitar.ucsd.edu/rcpy/rcpy.pdf)
  
## Author:

[Mauricio C. de Oliveira](http://control.ucsd.edu/mauricio)
