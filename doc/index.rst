.. rcpy documentation master file, created by
   sphinx-quickstart on Sat May 20 09:36:24 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

========================================================
Python 3 Interface for Robotics Cape and Beaglebone Blue
========================================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Introduction
============

This package supports the hardware on the `Robotics Cape
<http://www.strawsondesign.com/>`_ running on a `Beaglebone Black
<https://beagleboard.org/black>`_ or a `Beaglebone Blue
<https://beagleboard.org/blue>`_.

Installation
------------

See `<http://github.com/mcdeoliveira/rcpy#installation>`_ for installation instructions.

.. _rcpy:

Module `rcpy`
=============

.. py:module:: rcpy

This module is responsible to loading and initializing all hardware
devices associated with the Robotics Cape or Beagelbone Blue. Just type::

    import rcpy

to load the module. After loading the Robotics Cape is left at the
state :py:data:`rcpy.PAUSED`. It will also automatically cleanup after
you exit your program. You can add additional function to be called by
the cleanup routine using :py:func:`rcpy.add_cleanup`.

Constants
---------

.. py:data:: IDLE

.. py:data:: RUNNING

.. py:data:: PAUSED
   
.. py:data:: EXITING
	       
Low-level functions
-------------------

.. py:function:: get_state()

   Get the current state, one of :py:data:`rcpy.IDLE`, :py:data:`rcpy.RUNNING`, :py:data:`rcpy.PAUSED`, :py:data:`rcpy.EXITING`.

.. py:function:: set_state(state)

   Set the current state, `state` is one of :py:data:`rcpy.IDLE`, :py:data:`rcpy.RUNNING`, :py:data:`rcpy.PAUSED`, :py:data:`rcpy.EXITING`.
   
.. py:function:: exit()

   Set state to :py:data:`rcpy.EXITING`.

.. py:function:: add_cleanup(fun, pars)

   :param fun: function to call at cleanup
   :param pars: list of positional parameters to pass to function `fun`
		 
   Add function `fun` and parameters `pars` to the list of cleanup functions.
   
.. _rcpy_gpio:

Module `rcpy.gpio`
==================

.. py:module:: rcpy.gpio

This module provides an interface to the GPIO pins used by the
Robotics Cape. There are low level functions which closely mirror the
ones available in the C library and also Classes that provide a higher
level interface.

For example::

    import rcpy.gpio as gpio
    pause_button = gpio.Input(gpio.PAUSE_BTN)

imports the module and create an :py:class:`rcpy.gpio.Input` object
corresponding to the *PAUSE* button on the Robotics Cape. The
command::
    
    if pause_button.low():
      print('Got <PAUSE>!')

waits forever until the *PAUSE* button on the Robotics Cape is pressed
and::

    try:
        if pause_button.low(timeout = 2000):
            print('Got <PAUSE>!')
    except gpio.InputTimeout:
        print('Timed out!')

waits for at most 2000 ms, i.e. 2 s, before giving up.

This module also provides the class :py:class:`rcpy.gpio.InputEvent` to
handle input events. For example::

    class MyInputEvent(gpio.InputEvent):

        def action(self, event):
            print('Got <PAUSE>!')

defines a class that can be used to print :samp:`Got <PAUSE>!` every
time an input event happens. To connect this class with the particular
event that the *PAUSE* button is pressed instantiate::

    pause_event = MyInputEvent(pause_button, gpio.InputEvent.LOW)

which will cause the method `action` of the `MyInputEvent` class be
called every time the state of the `pause_button` becomes
:py:data:`rcpy.gpio.LOW`. The event handler must be started by
calling::

    pause_event.start()
    
and it can be stopped by::
  
    pause_event.stop()

Alternatively one could have created an input event handler by passing
a function to the argument `target` of
:py:class:`rcpy.gpio.InputEvent` as in::

    def pause_action(input, event):
        if event == gpio.InputEvent.LOW:
            print('<PAUSE> went LOW')
        elif event == gpio.InputEvent.HIGH:
            print('<PAUSE> went HIGH')
	    
    pause_event = gpio.InputEvent(pause_button,
                                  gpio.InputEvent.LOW | gpio.InputEvent.HIGH,
				  target = pause_action)

Note that the function `pause_action` will be called when
`pause_button` becomes either :py:data:`rcpy.gpio.HIGH` or
:py:data:`rcpy.gpio.LOW` because the event passed to the the
constructor :py:class:`InputEvent` is::

    gpio.InputEvent.LOW | gpio.InputEvent.HIGH

which is joined by the logical or operator `|`. The function
`pause_action` decides on the type of event by checking the variable
`event`. This event handler should be started and stopped using
:py:meth:`rcpy.gpio.InputEvent.start` and
:py:meth:`rcpy.gpio.InputEvent.stop` as before.

Additional positional or keyword arguments can be passed as in::

    def pause_action_with_parameter(input, event, parameter):
        print('Got <PAUSE> with {}!'.format(parameter))
	    
    pause_event = gpio.InputEvent(pause_button, gpio.InputEvent.LOW,
                                  target = pause_action_with_parameter,
				  vargs = ('some parameter',))

See also :py:class:`rcpy.button.Button` for a better interface for
working with the Robotics Cape buttons.

Constants
---------

.. py:data:: HIGH
	     
   Logic high level; equals `1`.
	     
.. py:data:: LOW
	     
   Logic low level; equals `0`.

.. py:data:: POLL_TIMEOUT
	     
   Timeout in ms to be used when polling GPIO input (Default 100ms)

.. py:data:: DEBOUNCE_INTERVAL
	     
   Interval in ms to be used for debouncing (Default 0.5ms)
   
Classes
-------

.. py:class:: InputTimeout()

   Exception representing an input timeout event.

.. py:class:: Input(pin)

   :param int pin: GPIO pin

   :py:class:`rcpy.gpio.Input` represents one of the GPIO input pins in the Robotics Cape or Beaglebone Blue.

   .. py:method:: is_high()

      :returns: :samp:`True` if pin is equal to :py:data:`rcpy.gpio.HIGH` and :samp:`False` if pin is :py:data:`rcpy.gpio.LOW`

   .. py:method:: is_low()

      :returns: :samp:`True` if pin is equal to :py:data:`rcpy.gpio.LOW` and :samp:`False` if pin is :py:data:`rcpy.gpio.HIGH`
      
   .. py:method:: high_or_low(debounce = 0, timeout = None)
                   
      :param int debounce: number of times to read input for debouncing (default 0)
      :param int timeout: timeout in milliseconds (default None)
      :raises rcpy.gpio.InputTimeout: if more than `timeout` ms have elapsed without the input changing

      :returns: the new state as :py:data:`rcpy.gpio.HIGH` or :py:data:`rcpy.gpio.LOW`

      Wait for pin to change state.
      
      If `timeout` is not :samp:`None` wait at most `timeout` ms.

      If `timeout` is negative wait forever. This call cannot be interrupted.
      
      If `timeout` is :samp:`None` wait forever by repeatedly polling in :py:data:`rcpy.gpio.POLL_TIMEOUT` ms. This call can only be interrupted by calling :py:func:`rcpy.exit`.

   .. py:method:: high(debounce = 0, timeout = None)

      :param int debounce: number of times to read input for debouncing (default 0)
      :param int timeout: timeout in milliseconds (default None)
      :raises rcpy.gpio.InputTimeout: if more than `timeout` ms have elapsed without the input changing

      :returns: :samp:`True` if the new state is :py:data:`rcpy.gpio.HIGH` and :samp:`False` if the new state is :py:data:`rcpy.gpio.LOW`
	 
      Wait for pin to change state.

      If `timeout` is not :samp:`None` wait at most `timeout` ms.

      If `timeout` is negative wait forever. This call cannot be interrupted.
      
      If `timeout` is :samp:`None` wait forever by repeatedly polling in :py:data:`rcpy.gpio.POLL_TIMEOUT` ms. This call can only be interrupted by calling :py:func:`rcpy.exit`.

   .. py:method:: low(debounce = 0, timeout = None)

      :param int debounce: number of times to read input for debouncing (default 0)
      :param int timeout: timeout in milliseconds (default None)
      :raises rcpy.gpio.InputTimeout: if more than `timeout` ms have elapsed without the input changing

      :returns: :samp:`True` if the new state is :py:data:`rcpy.gpio.LOW` and :samp:`False` if the new state is :py:data:`rcpy.gpio.HIGH`
				      
      Wait for pin to change state.

      If `timeout` is not :samp:`None` wait at most `timeout` ms.

      If `timeout` is negative wait forever. This call cannot be interrupted.
      
      If `timeout` is :samp:`None` wait forever by repeatedly polling in :py:data:`rcpy.gpio.POLL_TIMEOUT` ms. This call can only be interrupted by calling :py:func:`rcpy.exit`.
			  
.. py:class:: InputEvent(input, event, debounce = 0, timeout = None, target = None, vargs = (), kwargs = {})

   :bases: threading.Thread

   :py:class:`rcpy.gpio.InputEvent` is an event handler for GPIO input events.

   :param int input: instance of :py:class:`rcpy.gpio.Input`
   :param int event: either :py:data:`rcpy.gpio.InputEvent.HIGH` or :py:data:`rcpy.gpio.InputEvent.LOW`
   :param int debounce: number of times to read input for debouncing (default 0)
   :param int timeout: timeout in milliseconds (default None)
   :param int target: callback function to run in case input changes (default None)
   :param int vargs: positional arguments for function `target` (default ())
   :param int kwargs: keyword arguments for function `target` (default {})

   .. py:data:: LOW

      Event representing change to a low logic level.
		 
   .. py:data:: HIGH

      Event representing change to a high logic level.

   .. py:method:: action(event, *vargs, **kwargs)

      :param event: either :py:data:`rcpy.gpio.HIGH` or :py:data:`rcpy.gpio.LOW`
      :param vargs: variable positional arguments
      :param kwargs: variable keyword arguments

      Action to perform when event is detected.
            
   .. py:method:: start()

      Start the input event handler thread.
      
   .. py:method:: stop()

      Attempt to stop the input event handler thread. Once it has stopped it cannot be restarted.

Low-level functions
-------------------

.. py:function:: set(pin, value)

   :param int pin: GPIO pin
   :param int value: value to set the pin (:py:data:`rcpy.gpio.HIGH` or :py:data:`rcpy.gpio.LOW`)
   :raises rcpy.gpio.error: if it cannot write to `pin`

   Set GPIO `pin` to the new `value`.
		     
.. py:function:: get(pin)

   :param int pin: GPIO pin
   :raises rcpy.gpio.error: if it cannot read from `pin`
   :returns: the current value of the GPIO `pin`

   This is a non-blocking call.

.. py:function:: read(pin, timeout = None)

   :param int pin: GPIO pin
   :param int timeout: timeout in milliseconds (default None)
   :raises rcpy.gpio.error: if it cannot read from `pin`
   :raises rcpy.gpio.InputTimeout: if more than `timeout` ms have elapsed without the input changing
   :returns: the new value of the GPIO `pin`

   Wait for value of the GPIO `pin` to change. This is a blocking call.

.. _rcpy_button:

Module `rcpy.button`
====================

.. py:module:: rcpy.button

This module provides an interface to the *PAUSE* and *MODE* buttons in
the Robotics Cape. The command::

    import rcpy.button as button

imports the module. The :ref:`rcpy_button` provides objects
corresponding to the *PAUSE* and *MODE* buttons on the Robotics
Cape. Those are :py:data:`rcpy.button.pause` and
:py:data:`rcpy.button.mode`. One can import those objects directly
using::

    from rcpy.button import mode, pause

After importing these objects::
    
    if mode.pressed():
        print('<MODE> pressed!')

waits forever until the *MODE* button on the Robotics Cape is pressed and::

    if mode.released():
        print('<MODE> released!')

waits forever until the *MODE* button on the Robotics Cape is
released. Note that nothing will print if you first have to press the
button before releasing because :py:meth:`rcpy.button.Button.released`
returns :samp:`False` after the first input event, which in this case
was :py:data:`rcpy.button.PRESSED`.

As with :ref:`rcpy_gpio`, it is possible to use
:py:class:`rcpy.gpio.InputTimeout` as in::

    import rcpy.gpio as gpio
    try:
        if mode.pressed(timeout = 2000):
            print('<MODE> pressed!')
    except gpio.InputTimeout:
        print('Timed out!')

which waits for at most 2000 ms, i.e. 2 s, before giving up.

This module also provides the class :py:class:`rcpy.button.ButtonEvent` to
handle input events. For example::

    class MyButtonEvent(button.ButtonEvent):

        def action(self, event):
            print('Got <PAUSE>!')

defines a class that can be used to print :samp:`Got <PAUSE>!` every
time the *PAUSE* button is pressed. To instantiate and start the event
handler use::

    pause_event = MyButtonEvent(pause, button.ButtonEvent.PRESSED)
    pause_event.start()

Note that the event :py:data:`button.ButtonEvent.PRESSED` was used so
that :py:meth:`MyButtonEvent.action` is called only when the *PAUSE*
button is pressed. It may be convenient to import these events::

    from rcpy.button import PRESSED, RELEASED
    
The event handler can be stopped by calling::
  
    pause_event.stop()

Alternatively one could have created an input event handler by passing
a function to the argument `target` of
:py:class:`rcpy.button.ButtonEvent` as in::

    def pause_action(input, event):
        if event == PRESSED:
            print('<PAUSE> pressed!')
        elif event == RELEASED:
            print('<PAUSE> released!')
	    
    pause_event = button.ButtonEvent(pause, PRESSED | RELEASED,
			             target = pause_action)

This event handler should be started and stopped using
:py:meth:`rcpy.button.ButtonEvent.start` and
:py:meth:`rcpy.button.ButtonEvent.stop` as in
:ref:`rcpy_gpio`. Additional positional or keyword arguments can be
passed as in::

    def pause_action_with_parameter(input, event, parameter):
        print('Got <PAUSE> with {}!'.format(parameter))
	    
    pause_event = button.ButtonEvent(pause, PRESSED,
                                     target = pause_action_with_parameter,
				     vargs = ('some parameter',))

The main difference between :ref:`rcpy_button` and :ref:`rcpy_gpio` is
that :ref:`rcpy_button` defines the constants
:py:data:`rcpy.button.PRESSED` and :py:data:`rcpy.button.RELEASED`,
the events :py:data:`rcpy.button.ButtonEvent.PRESSED` and
:py:data:`rcpy.button.ButtonEvent.RELEASED`, and its classes handle
debouncing by default.

Constants
---------

.. py:data:: pause
	     
   :py:class:`rcpy.button.Button` representing the Robotics Cape *PAUSE* button.

.. py:data:: mode
	     
   :py:class:`rcpy.button.Button` representing the Robotics Cape *MODE* button.
       
.. py:data:: PRESSED
	     
   State of a pressed button; equal to :py:data:`rcpy.gpio.LOW`.
	     
.. py:data:: RELEASED
	     
   State of a released button; equal to :py:data:`rcpy.gpio.HIGH`.

.. py:data:: DEBOUNCE
	     
   Number of times to test for deboucing (Default 3)

Classes
-------
	     	     
.. py:class:: Button()

   :bases: :py:class:`rcpy.gpio.Input`
	   
   :py:class:`rcpy.button.Button` represents buttons in the Robotics Cape or Beaglebone Blue.
	   
   .. py:method:: is_pressed(debounce = rcpy.button.DEBOUNCE, timeout = None)

      :returns: :samp:`True` if button state is equal to :py:data:`rcpy.gpio.PRESSED` and :samp:`False` if pin is :py:data:`rcpy.gpio.RELEASED`
		  
   .. py:method:: is_released(debounce = rcpy.button.DEBOUNCE, timeout = None)
    
      :returns: :samp:`True` if button state is equal to :py:data:`rcpy.gpio.RELEASED` and :samp:`False` if pin is :py:data:`rcpy.gpio.PRESSED`  
		  
   .. py:method:: pressed_or_released(debounce = rcpy.button.DEBOUNCE, timeout = None)

      :param int debounce: number of times to read input for debouncing (default `rcpy.button.DEBOUNCE`)
      :param int timeout: timeout in milliseconds (default None)
      :raises rcpy.gpio.InputTimeout: if more than `timeout` ms have elapsed without the button state changing

      :returns: the new state as :py:data:`rcpy.button.PRESSED` or :py:data:`rcpy.button.RELEASED`
		
      Wait for button state to change.

      If `timeout` is not :samp:`None` wait at most `timeout` ms.

      If `timeout` is negative wait forever. This call cannot be interrupted.
      
      If `timeout` is :samp:`None` wait forever by repeatedly polling in :py:data:`rcpy.gpio.POLL_TIMEOUT` ms. This call can only be interrupted by calling :py:func:`rcpy.exit`.
      
   .. py:method:: pressed(debounce = rcpy.button.DEBOUNCE, timeout = None)

      :param int debounce: number of times to read input for debouncing (default `rcpy.button.DEBOUNCE`)
      :param int timeout: timeout in milliseconds (default None)
      :raises rcpy.gpio.InputTimeout: if more than `timeout` ms have elapsed without the button state changing.

      :returns: :samp:`True` if the new state is :py:data:`rcpy.button.PRESSED` and :samp:`False` if the new state is :py:data:`rcpy.button.RELEASED` 
				      
      Wait for button state to change.
      
      If `timeout` is not :samp:`None` wait at most `timeout` ms.

      If `timeout` is negative wait forever. This call cannot be interrupted.
      
      If `timeout` is :samp:`None` wait forever by repeatedly polling in :py:data:`rcpy.gpio.POLL_TIMEOUT` ms. This call can only be interrupted by calling :py:func:`rcpy.exit`.
      
   .. py:method:: released(debounce = rcpy.button.DEBOUNCE, timeout = None)

      :param int debounce: number of times to read input for debouncing (default `rcpy.button.DEBOUNCE`)
      :param int timeout: timeout in milliseconds (default None)
      :raises rcpy.gpio.InputTimeout: if more than `timeout` ms have elapsed without the button state changing.
				      
      :returns: :samp:`True` if the new state is :py:data:`rcpy.button.RELEASED` and :samp:`False` if the new state is :py:data:`rcpy.button.PRESSED`

      Wait for button state to change.
		  
      If `timeout` is not :samp:`None` wait at most `timeout` ms.

      If `timeout` is negative wait forever. This call cannot be interrupted.
      
      If `timeout` is :samp:`None` wait forever by repeatedly polling in :py:data:`rcpy.gpio.POLL_TIMEOUT` ms. This call can only be interrupted by calling :py:func:`rcpy.exit`.
      
.. py:class:: ButtonEvent(input, event, debounce = rcpy.button.DEBOUNCE, timeout = None, target = None, vargs = (), kwargs = {})

   :bases: :py:class:`rcpy.gpio.InputEvent`

   :param int input: instance of :py:class:`rcpy.gpio.Input`
   :param int event: either :py:data:`rcpy.button.ButtonEvent.PRESSED` or :py:data:`rcpy.button.ButtonEvent.RELEASED`
   :param int debounce: number of times to read input for debouncing (default `rcpy.button.DEBOUNCE`)
   :param int timeout: timeout in milliseconds (default `None`)
   :param int target: callback function to run in case input changes (default `None`)
   :param int vargs: positional arguments for function `target` (default `()`)
   :param int kwargs: keyword arguments for function `target` (default `{}`)
	   
   :py:class:`rcpy.button.ButtonEvent` is an event handler for button events.

   .. py:data:: PRESSED

      Event representing pressing a button; equal to :py:data:`rcpy.gpio.InputEvent.LOW`.
		 
   .. py:data:: RELEASED

      Event representing releasing a button; equal to :py:data:`rcpy.gpio.InputEvent.HIGH`.

   .. py:method:: action(event, *vargs, **kwargs)

      :param event: either :py:data:`rcpy.button.PRESSED` or :py:data:`rcpy.button.RELEASED`
      :param vargs: variable positional arguments
      :param kwargs: variable keyword arguments
		     
      Action to perform when event is detected.
            
   .. py:method:: start()

      Start the input event handler thread.
      
   .. py:method:: stop()

      Attempt to stop the input event handler thread. Once it has stopped it cannot be restarted.

      
.. _rcpy_led:

Module `rcpy.led`
=================

.. py:module:: rcpy.led

This module provides an interface to the *RED* and *GREEN* buttons in
the Robotics Cape. The command::

    import rcpy.led as led

imports the module. The :ref:`rcpy_led` provides objects corresponding
to the *RED* and *GREEN* buttons on the Robotics Cape, namely
:py:data:`rcpy.led.red` and :py:data:`rcpy.led.green`. For example::
    
    led.red.on()

turns the *RED* LED on and::

    led.green.off()

turns the *GREEN* LED off. Likewise::

    led.green.is_on()

returns :samp:`True` if the *GREEN* LED is on and::

    led.red.is_off()

returns :samp:`True` if the *RED* LED is off.

This module also provides the class :py:class:`rcpy.led.Blink` to
handle LED blinking. It spawns a thread that will keep LEDs blinking
with a given period. For example::

    blink = led.Blink(led.red, .5)
    blink.start()

starts blinking the *RED* LED every 0.5 seconds. One can stop or
resume blinking by calling :py:meth:`rcpy.led.Blink.toggle` as in::

    blink.toggle()

or call::

    blink.stop()

to permanently stop the blinking thread.

One can also instantiate an :py:class:`rcpy.led.Blink` object by calling
:py:meth:`rcpy.led.LED.blink` as in::

    blink = led.red.blink(.5)

which returns an instance of
:py:class:`rcpy.led.Blink`. :py:meth:`rcpy.led.LED.blink`
automatically calls :py:meth:`rcpy.led.Blink.start`.

Constants
---------

.. py:data:: red
	     
   :py:class:`rcpy.led.LED` representing the Robotics Cape *RED* LED.

.. py:data:: green
	     
   :py:class:`rcpy.led.LED` representing the Robotics Cape *GREEN* LED.
       
.. py:data:: ON
	     
   State of an on LED; equal to :py:data:`rcpy.gpio.HIGH`.
	     
.. py:data:: OFF
	     
   State of an off led; equal to :py:data:`rcpy.gpio.LOW`.

Classes
-------

.. py:class:: LED(output, state = rcpy.led.OFF)

   :bases: :py:class:`rcpy.gpio.Output`
	   
   :param output: GPIO pin
   :param state: initial LED state
	      
   :py:class:`rcpy.led.LED` represents LEDs in the Robotics Cape or Beaglebone Blue.
       
   .. py:method:: is_on()

      :returns: :samp:`True` if LED is on and :samp:`False` if LED is off
		  
   .. py:method:: is_off()
            
      :returns: :samp:`True` if LED is off and :samp:`False` if LED is on

   .. py:method:: on()

      Change LED state to :py:data:`rcpy.LED.ON`.

   .. py:method:: off()

      Change LED state to :py:data:`rcpy.LED.OFF`.
		  
   .. py:method:: toggle()

      Toggle current LED state.
   
   .. py:method:: blink(period)

      :param float period: period of blinking
      :returns: an instance of :py:class:`rcpy.led.Blink`.

      Blinks LED with a period of `period` seconds.
		  
.. py:class:: Blink(led, period)

   :bases: threading.Thread

   .. py:method:: set_period(period)

      :param float period: period of blinking

      Set blinking period.
		  
   .. py:method:: toggle()

      Toggle blinking on and off. Call toggle again to resume or stop blinking.

   .. py:method:: start()

      Start the blinking thread.
    
   .. py:method:: stop()

      Stop the blinking thread. Blinking cannot resume after calling :py:meth:`rcpy.led.Blink.stop`.
		  
.. _rcpy_encoder:
   
Module `rcpy.encoder`
=====================

.. py:module:: rcpy.encoder

This module provides an interface to the four *encoder channels* in
the Robotics Cape. The command::

    import rcpy.encoder as encoder

imports the module. The :ref:`rcpy_encoder` provides objects
corresponding to the each of the encoder channels on the Robotics
Cape, namely :py:data:`rcpy.encoder.encoder1`,
:py:data:`rcpy.encoder.encoder2`, :py:data:`rcpy.encoder.encoder3`,
and :py:data:`rcpy.encoder.encoder4`. It may be convenient to import
one or all of these objects as in ::

    from rcpy.encoder import encoder1

The current encoder count can be obtained using::

    encoder1.get()

One can also *reset* the count to zero using::

    encoder1.reset()

or to an arbitrary count using::

    encode1.set(1024)

Constants
---------

.. py:data:: encoder1

   :py:class:`rcpy.encoder.Encoder` representing the Robotics Cape *Encoder 1*.

.. py:data:: encoder2

   :py:class:`rcpy.encoder.Encoder` representing the Robotics Cape *Encoder 2*.
       
.. py:data:: encoder3

   :py:class:`rcpy.encoder.Encoder` representing the Robotics Cape *Encoder 3*.
       
.. py:data:: encoder4

   :py:class:`rcpy.encoder.Encoder` representing the Robotics Cape *Encoder 4*.
	       
Classes
-------

.. py:class:: Encoder(channel, count = None)

   :param output: encoder channel (1 through 4)
   :param state: initial encoder count (Default None)
	      
   :py:class:`rcpy.encoder.Encoder` represents encoders in the Robotics Cape or Beaglebone Blue.
       
   .. py:method:: get()

      :returns: current encoder count
		  
   .. py:method:: set(count)
            
      Set current encoder count to `count`.

   .. py:method:: reset()
            
      Set current encoder count to `0`.
      
Low-level functions
-------------------

.. py:function:: get(channel)

   :param int channel: encoder channel number

   :returns: current encoder count

   This is a non-blocking call.
   
.. py:function:: set(channel, count = 0)

   :param int channel: encoder channel number
   :param int count: desired encoder count

   Set encoder `channel` count to `value`.
		     
.. _rcpy_motor:

Module `rcpy.motor`
===================

.. py:module:: rcpy.motor

This module provides an interface to the four *motor channels* in the
Robotics Cape. Those control a high power PWM (Pulse Width Modulation)
signal which is typically used to control *DC Motors*. The command::

    import rcpy.motor as motor

imports the module. The :ref:`rcpy_motor` provides objects
corresponding to the each of the motor channels on the Robotics Cape,
namely :py:data:`rcpy.motor.motor1`, :py:data:`rcpy.motor.motor2`,
:py:data:`rcpy.motor.motor3`, and :py:data:`rcpy.motor.motor4`. It may
be convenient to import one or all of these objects as in ::

    from rcpy.motor import motor1

The current average voltage applied to the motor can be set using::

    duty = 1
    motor1.set(duty)

where `duty` is a number varying from -1 to 1 which controls the
percentage of the voltage available to the Robotics Cape that should
be applied on the motor. A motor can be turned off by::

    motor1.set(0)

or using one of the special methods
:py:meth:`rcpy.motor.Motor.free_spin` or
:py:meth:`rcpy.motor.Motor.brake`, which can be used to turn off the
motor and set it in a *free-spin* or *braking* configuration. For
example::

    motor1.free_spin()

puts :py:data:`motor1` in *free-spin* mode. In *free-spin mode* the
motor behaves as if there were no voltage applied to its terminal,
that is it is allowed to spin freely. In *brake mode* the terminals of
the motor are *short-circuited* and the motor winding will exert an
opposing force if the motor shaft is moved.

Constants
---------

.. py:data:: motor1

   :py:class:`rcpy.motor.Motor` representing the Robotics Cape *Motor 1*.

.. py:data:: motor2

   :py:class:`rcpy.motor.Motor` representing the Robotics Cape *Motor 2*.
       
.. py:data:: motor3

   :py:class:`rcpy.motor.Motor` representing the Robotics Cape *Motor 3*.
       
.. py:data:: motor4

   :py:class:`rcpy.motor.Motor` representing the Robotics Cape *Motor 4*.
	       
Classes
-------

.. py:class:: Motor(channel, duty = None)

   :param output: motor channel (1 through 4)
   :param state: initial motor duty cycle (Default None)
	      
   :py:class:`rcpy.motor.Motor` represents motors in the Robotics Cape or Beaglebone Blue.
       
   .. py:method:: set(duty)
            
      Set current motor duty cycle to `duty`. `duty` is a number between -1 and 1.

   .. py:method:: free_spin()
            
      Stops the motor and puts it in *free-spin* mode.

   .. py:method:: brake()
            
      Stops the motor and puts it in *brake* mode.      
      
Low-level functions
-------------------

.. py:function:: set(channel, duty)

   :param int channel: motor channel number
   :param int duty: desired motor duty cycle

   Sets the motor channel `channel` duty cycle to `duty`.

   This is a non-blocking call.
		    
.. py:function:: set_free_spin(channel)

   :param int channel: motor channel number

   Puts the motor channel `channel` in *free-spin mode*.
		       
   This is a non-blocking call.
	       
.. py:function:: set_brake(channel)

   :param int channel: motor channel number

   Puts the motor channel `channel` in *brake mode*.
		       
   This is a non-blocking call.

.. _rcpy_mpu9250:

Module `rcpy.mpu9250`
=====================

.. py:module:: rcpy.mpu9250


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
