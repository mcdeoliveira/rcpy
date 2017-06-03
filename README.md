# rcpy: Python 3 Interface for the Robotics Cape on the Beaglebone Black and the Beaglebone Blue

**Release 0.3**

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

## Preliminaries

You will need the
[Robotics Cape library](https://github.com/StrawsonDesign/Robotics_Cape_Installer)
version 0.3.4 or higher. Depending on the image you have on your
Beaglebone Black or Blue it might already be installed! You can check
if it is installed and the current version by running

    rc_version
	
on your Beaglebone. Follow these
[instructions](http://strawsondesign.com/#!manual-install) if the
command `rc_version` is not found to install the library or update it
if you have an older version.

You must also have python3 installed. If you have not installed
python3 yet type

    sudo apt install python3 python3-pip

to install python3 and pip3.

## Installation

Starting with version 0.3 rcpy is available from PyPI. Just type

    sudo pip3 install rcpy
	
to download and install the package.

## Available Documentation:

* [HTML](http://guitar.ucsd.edu/rcpy/html/index.html)

* [PDF](http://guitar.ucsd.edu/rcpy/rcpy.pdf)
  
## Author:

[Mauricio C. de Oliveira](http://control.ucsd.edu/mauricio)
