rcpy: Python 3 Interface for the Robotics Cape on the Beaglebone Black and the Beaglebone Blue
==============================================================================================

**Release 0.4**

This is a Python library with bindings for some of the functionality of
the `Robotics Cape
library <https://github.com/StrawsonDesign/Robotics_Cape_Installer>`__.

We only support Python 3, and are not interested in Python 2 at all.

Not all functions are supported. Currently supported functions are:

1. MPU9250
2. PWM motors
3. Servos and ESCs
4. Encoders
5. LEDs
6. Buttons
7. GPIO inputs

You might also be interested in the ``pyctrl`` package
(`github <https://github.com/mcdeoliveira/pyctrl>`__,
`PyPI <https://pypi.python.org/pypi?:action=display&name=pyctrl>`__).

Preliminaries
-------------

You will need the `Robotics Cape
library <https://github.com/StrawsonDesign/Robotics_Cape_Installer>`__
version 0.3.4 or higher. Depending on the image you have on your
Beaglebone Black or Blue it might already be installed! You can check if
it is installed and the current version by running

::

    rc_version

on your Beaglebone. If the command ``rc_version`` is not found type

::

    sudo apt-get update
    sudo apt-get install roboticscape

to install or

::

    sudo apt-get update
    sudo apt-get upgrade roboticscape

to upgrade from an older version. For more details see these
`instructions <http://strawsondesign.com/#!manual-install>`__.

You must also have python3 installed. If you have not installed python3
yet type

::

    sudo apt install python3 python3-pip

to install python3 and pip3.

Installation
------------

Starting with version 0.3, ``rcpy`` is available from
`PyPI <https://pypi.python.org/pypi?:action=display&name=rcpy>`__. Just
type

::

    sudo pip3 install rcpy

to download and install.

Documentation:
--------------

-  `HTML <http://guitar.ucsd.edu/rcpy/html/index.html>`__

-  `PDF <http://guitar.ucsd.edu/rcpy/rcpy.pdf>`__

Author:
-------

`Mauricio C. de Oliveira <http://control.ucsd.edu/mauricio>`__
