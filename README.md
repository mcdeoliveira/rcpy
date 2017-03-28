# rcpy: Python bindings for roboticscape

This is a Python library with bindings for some of the functionality of the [Robotics Cape library](https://github.com/StrawsonDesign/Robotics_Cape_Installer).

We only support Python 3, although there is nothing that I can see that would prevent it from compiling under Python 2 as well.

Not all functions are supported. Currently supported functions are:

1. MPU9250
2. PWM motors
3. Encoders

You might also be interested in the [ctrl package](https://github.com/mcdeoliveira/ctrl).

## Installation

As of today you will need a modified version of the current Robotics
Cape library. You can clone it from the fork:

    git clone https://github.com/mcdeoliveira/Robotics_Cape_Installer

Make sure you compile and install the modified version of the library:

    cd Robotics_Cape_Installer/libraries
    make clean
    make install

Clone this repository:

    git clone https://github.com/mcdeoliveira/rcpy

Run setup.py install:

    python3 setup.py install

## Author:

[Mauricio C. de Oliveira](https://control.ucsd.edu/mauricio)