Modules
=======

.. _rcpy:

Module `rcpy`
-------------

.. py:module:: rcpy

This module is responsible to loading and initializing all hardware
devices associated with the Robotics Cape or Beagelbone Blue. Just type::

    import rcpy

to load the module. After loading the Robotics Cape is left at the
state :py:data:`rcpy.PAUSED`. It will also automatically cleanup after
you exit your program. You can add additional function to be called by
the cleanup routine using :py:func:`rcpy.add_cleanup`.

Constants
^^^^^^^^^

.. py:data:: IDLE

.. py:data:: RUNNING

.. py:data:: PAUSED
   
.. py:data:: EXITING
	       
Low-level functions
^^^^^^^^^^^^^^^^^^^

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

Module `rcpy.clock`
-------------------

.. py:module:: rcpy.clock

This module provides a class :py:class:`rcpy.clock.Clock` that can be
used to run actions periodically. Actions must inherit from the class
:py:class:`rcpy.clock.Action` and implement the method
:py:meth:`rcpy.clock.Action.run`. Examples of objects that inherit
from :py:class:`rcpy.clock.Action` are :py:class:`rcpy.led.LED` and
:py:class:`rcpy.servo.Servo`.

For example::

    import rcpy.clock as clock
    from rcpy.led import red
    clk = clock.Clock(red)
    clk.start()

will start a *thread* that will blink the *red* LED every second. The
command::

    clk.stop()

will stop the LED blinking. The subclass :py:class:`rcpy.led.Blink`
will in addition turn off the led after stopping.

Classes
^^^^^^^

.. py:class:: Action()

   :py:class:`rcpy.clock.Action` represents and action.
	      
   .. py:method:: run()

      Run the action.

.. py:class:: Actions(*actions)

   :bases: :py:class:`rcpy.clock.Action`
	      
   :py:class:`rcpy.clock.Actions` represents a sequence of actions.

   :param actions: comma separated list of actions.
	      
.. py:class:: Clock(action, period)

   :bases: threading.Thread

   :py:class:`rcpy.clock.Clock` executes actions periodically.

   :param Action action: the action to be executed
   :param int period: the period in seconds (default 1 second)
	   
   .. py:method:: set_period(period)

      :param float period: period in seconds

      Set action period.
		  
   .. py:method:: toggle()

      Toggle action on and off. Call toggle again to resume or stop action.

   .. py:method:: start()

      Start the action thread.
    
   .. py:method:: stop()

      Stop the action thread. Action cannot resume after calling :py:meth:`rcpy.led.Blink.stop`. Use :py:meth:`rcpy.clock.Clock.toggle` to temporarily interrupt an action.


Module `rcpy.gpio`
------------------

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

waits forever until the *PAUSE* button on the Robotics Cape becomes
:py:data:`rcpy.gpio.LOW`, which happens when it is pressed. The
following slightly modified version::

    try:
        if pause_button.low(timeout = 2000):
            print('Got <PAUSE>!')
    except gpio.InputTimeout:
        print('Timed out!')

waits for at most 2000 ms, i.e. 2 s, before giving up, which one can
detect by catching the exception :py:class:`rcpy.gpio.InputTimeout`.

In the same vein, the method :py:meth:`rcpy.gpio.Input.high` would
wait for the button *PAUSE* to become :py:data:`rcpy.gpio.HIGH`. For
instance::

    if pause_button.high():
        print('<PAUSE> got high!')

waits forever until the *PAUSE* button on the Robotics Cape is
released. Note that nothing will print if you first have to press the
button before releasing because :py:meth:`rcpy.gpio.Input.high`
returns :samp:`False` after the first input event, which in this case
would correspond to the GPIO pin going :py:data:`rcpy.gpio.LOW`.

The methods :py:meth:`rcpy.gpio.Input.is_low` and
:py:meth:`rcpy.gpio.Input.is_high` are *non-blocking* versions of the
above methods. For example::

    import time
    while True:
        if pause_button.is_low():
            print('Got <PAUSE>!')
	    break
	time.sleep(1)

checks the status of the button *PAUSE* every 1 s and breaks when
*PAUSE* is pressed. A much better way to handle such events is to use
the class :py:class:`rcpy.gpio.InputEvent`. For example::

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

The event handler automatically runs on a separate *thread*, which
means that the methods :py:meth:`rcpy.gpio.InputEvent.start` and
:py:meth:`rcpy.gpio.InputEvent.stop` are *non-blocking*, that is they
return immediately.
    
The class :py:class:`rcpy.gpio.InputEvent` defines two types of
events: :py:data:`rcpy.gpio.InputEvent.HIGH` and
:py:data:`rcpy.gpio.InputEvent.LOW`. Note that these are not the same
as :py:data:`rcpy.gpio.HIGH` and :py:data:`rcpy.gpio.LOW`! It is often
convenient to import the base class :py:data:`rcpy.gpio.InputEvent`::

    from rcpy.gpio import InputEvent

Alternatively one could have created an input event handler by passing
a function to the argument `target` of
:py:class:`rcpy.gpio.InputEvent` as in::

    def pause_action(input, event):
        if event == InputEvent.LOW:
            print('<PAUSE> went LOW')
        elif event == InputEvent.HIGH:
            print('<PAUSE> went HIGH')
	    
    pause_event = InputEvent(pause_button,
                             InputEvent.LOW | InputEvent.HIGH,
			     target = pause_action)

The function `pause_action` will be called when `pause_button`
generates either event :py:data:`rcpy.gpio.InputEvent.HIGH` or
:py:data:`rcpy.gpio.InputEvent.LOW` because the events passed to the
the constructor :py:class:`InputEvent` were combined using the
*logical or* operator `|`, as in::

    InputEvent.LOW | InputEvent.HIGH,

The function `pause_action` decides on the type of event by checking
the variable `event`. This event handler should be started and stopped
using :py:meth:`rcpy.gpio.InputEvent.start` and
:py:meth:`rcpy.gpio.InputEvent.stop` as before.

Additional positional or keyword arguments can be passed as in::

    def pause_action_with_parameter(input, event, parameter):
        print('Got <PAUSE> with {}!'.format(parameter))
	    
    pause_event = InputEvent(pause_button, InputEvent.LOW,
                             target = pause_action_with_parameter,
			     vargs = ('some parameter',))

See also :py:class:`rcpy.button.Button` for a better interface for
working with the Robotics Cape buttons.

Constants
^^^^^^^^^

.. py:data:: HIGH
	     
   Logic high level; equals `1`.
	     
.. py:data:: LOW
	     
   Logic low level; equals `0`.

.. py:data:: DEBOUNCE_INTERVAL
	     
   Interval in ms to be used for debouncing (Default 0.5ms)
   
Classes
^^^^^^^

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
      
      If `timeout` is not :samp:`None` wait at most `timeout` ms otherwise wait forever until the input changes.


   .. py:method:: high(debounce = 0, timeout = None)

      :param int debounce: number of times to read input for debouncing (default 0)
      :param int timeout: timeout in milliseconds (default None)
      :raises rcpy.gpio.InputTimeout: if more than `timeout` ms have elapsed without the input changing

      :returns: :samp:`True` if the new state is :py:data:`rcpy.gpio.HIGH` and :samp:`False` if the new state is :py:data:`rcpy.gpio.LOW`
	 
      Wait for pin to change state.

      If `timeout` is not :samp:`None` wait at most `timeout` ms otherwise wait forever until the input changes.

   .. py:method:: low(debounce = 0, timeout = None)

      :param int debounce: number of times to read input for debouncing (default 0)
      :param int timeout: timeout in milliseconds (default None)
      :raises rcpy.gpio.InputTimeout: if more than `timeout` ms have elapsed without the input changing

      :returns: :samp:`True` if the new state is :py:data:`rcpy.gpio.LOW` and :samp:`False` if the new state is :py:data:`rcpy.gpio.HIGH`
				      
      Wait for pin to change state.

      If `timeout` is not :samp:`None` wait at most `timeout` ms otherwise wait forever until the input changes.
			  
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
^^^^^^^^^^^^^^^^^^^

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
--------------------

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
would correspond to the GPIO pin associated to the button going
:py:data:`rcpy.button.PRESSED`.

:py:meth:`rcpy.button.Button.pressed` and
:py:meth:`rcpy.button.Button.released` also raise the exception
:py:class:`rcpy.gpio.InputTimeout` if the argument `timeout` is used
as in::

    import rcpy.gpio as gpio
    try:
        if mode.pressed(timeout = 2000):
            print('<MODE> pressed!')
    except gpio.InputTimeout:
        print('Timed out!')

which waits for at most 2000 ms, i.e. 2 s, before giving up.

The methods :py:meth:`rcpy.button.Button.is_pressed` and
:py:meth:`rcpy.button.Button.is_released` are *non-blocking* versions
of the above methods. For example::

    import time
    while True:
        if mode.is_pressed():
            print('<Mode> pressed!')
	    break
	time.sleep(1)

checks the status of the button *MODE* every 1 s and breaks when
*MODE* is pressed. As with :ref:`rcpy_gpio`, a much better way to
handle such events is to use event handlers, in the case of
buttons the class :py:class:`rcpy.button.ButtonEvent`. For example::

    class MyButtonEvent(button.ButtonEvent):
        def action(self, event):
            print('Got <PAUSE>!')

defines a class that can be used to print :samp:`Got <PAUSE>!` every
time the *PAUSE* button is pressed. To instantiate and start the event
handler use::

    pause_event = MyButtonEvent(pause, button.ButtonEvent.PRESSED)
    pause_event.start()

Note that the event :py:data:`rcpy.button.ButtonEvent.PRESSED` was
used so that `MyButtonEvent.action` is called only when the *PAUSE*
button is pressed. The event handler can be stopped by calling::
  
    pause_event.stop()
   
Alternatively one could have created an input event handler by passing
a function to the argument `target` of
:py:class:`rcpy.button.ButtonEvent` as in::

    from rcpy.button import ButtonEvent
    
    def pause_action(input, event):
        if event == ButtonEvent.PRESSED:
            print('<PAUSE> pressed!')
        elif event == ButtonEvent.RELEASED:
            print('<PAUSE> released!')
	    
    pause_event = ButtonEvent(pause,
                              ButtonEvent.PRESSED | ButtonEvent.RELEASED,
			      target = pause_action)

This event handler should be started and stopped using
:py:meth:`rcpy.button.ButtonEvent.start` and
:py:meth:`rcpy.button.ButtonEvent.stop` as before. Additional
positional or keyword arguments can be passed as in::

    def pause_action_with_parameter(input, event, parameter):
        print('Got <PAUSE> with {}!'.format(parameter))
	    
    pause_event = ButtonEvent(pause, ButtonEvent.PRESSED,
                              target = pause_action_with_parameter,
		              vargs = ('some parameter',))

The main difference between :ref:`rcpy_button` and :ref:`rcpy_gpio` is
that :ref:`rcpy_button` defines the constants
:py:data:`rcpy.button.PRESSED` and :py:data:`rcpy.button.RELEASED`,
the events :py:data:`rcpy.button.ButtonEvent.PRESSED` and
:py:data:`rcpy.button.ButtonEvent.RELEASED`, and its classes handle
debouncing by default.

Constants
^^^^^^^^^

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
^^^^^^^
	     	     
.. py:class:: Button()

   :bases: :py:class:`rcpy.gpio.Input`
	   
   :py:class:`rcpy.button.Button` represents buttons in the Robotics Cape or Beaglebone Blue.
	   
   .. py:method:: is_pressed()

      :returns: :samp:`True` if button state is equal to :py:data:`rcpy.button.PRESSED` and :samp:`False` if pin is :py:data:`rcpy.button.RELEASED`
		  
   .. py:method:: is_released()
    
      :returns: :samp:`True` if button state is equal to :py:data:`rcpy.button.RELEASED` and :samp:`False` if pin is :py:data:`rcpy.button.PRESSED`  
		  
   .. py:method:: pressed_or_released(debounce = rcpy.button.DEBOUNCE, timeout = None)

      :param int debounce: number of times to read input for debouncing (default `rcpy.button.DEBOUNCE`)
      :param int timeout: timeout in milliseconds (default None)
      :raises rcpy.gpio.InputTimeout: if more than `timeout` ms have elapsed without the button state changing

      :returns: the new state as :py:data:`rcpy.button.PRESSED` or :py:data:`rcpy.button.RELEASED`
		
      Wait for button state to change.

      If `timeout` is not :samp:`None` wait at most `timeout` ms otherwise wait forever until the input changes.
      
   .. py:method:: pressed(debounce = rcpy.button.DEBOUNCE, timeout = None)

      :param int debounce: number of times to read input for debouncing (default `rcpy.button.DEBOUNCE`)
      :param int timeout: timeout in milliseconds (default None)
      :raises rcpy.gpio.InputTimeout: if more than `timeout` ms have elapsed without the button state changing.

      :returns: :samp:`True` if the new state is :py:data:`rcpy.button.PRESSED` and :samp:`False` if the new state is :py:data:`rcpy.button.RELEASED` 
				      
      Wait for button state to change.
      
      If `timeout` is not :samp:`None` wait at most `timeout` ms otherwise wait forever until the input changes.
      
   .. py:method:: released(debounce = rcpy.button.DEBOUNCE, timeout = None)

      :param int debounce: number of times to read input for debouncing (default `rcpy.button.DEBOUNCE`)
      :param int timeout: timeout in milliseconds (default None)
      :raises rcpy.gpio.InputTimeout: if more than `timeout` ms have elapsed without the button state changing.
				      
      :returns: :samp:`True` if the new state is :py:data:`rcpy.button.RELEASED` and :samp:`False` if the new state is :py:data:`rcpy.button.PRESSED`

      Wait for button state to change.
		  
      If `timeout` is not :samp:`None` wait at most `timeout` ms otherwise wait forever until the input changes.
      
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
-----------------

.. py:module:: rcpy.led

This module provides an interface to the *RED* and *GREEN* buttons in
the Robotics Cape. The command::

    import rcpy.led as led

imports the module. The :ref:`rcpy_led` provides objects corresponding
to the *RED* and *GREEN* buttons on the Robotics Cape, namely
:py:data:`rcpy.led.red` and :py:data:`rcpy.led.green`. It may be
convenient to import one or all of these objects as in::

    from rcpy.led import red, green

For example::
    
    red.on()

turns the *RED* LED on and::

    green.off()

turns the *GREEN* LED off. Likewise::

    green.is_on()

returns :samp:`True` if the *GREEN* LED is on and::

    red.is_off()

returns :samp:`True` if the *RED* LED is off.

This module also provides the class :py:class:`rcpy.led.Blink` to
handle LED blinking. It spawns a thread that will keep LEDs blinking
with a given period. For example::

    blink = led.Blink(red, .5)
    blink.start()

starts blinking the *RED* LED every 0.5 seconds. One can stop or
resume blinking by calling :py:meth:`rcpy.led.Blink.toggle` as in::

    blink.toggle()

or call::

    blink.stop()

to permanently stop the blinking thread.

One can also instantiate an :py:class:`rcpy.led.Blink` object by calling
:py:meth:`rcpy.led.LED.blink` as in::

    blink = red.blink(.5)

which returns an instance of
:py:class:`rcpy.led.Blink`. :py:meth:`rcpy.led.LED.blink`
automatically calls :py:meth:`rcpy.led.Blink.start`.

Constants
^^^^^^^^^

.. py:data:: red
	     
   :py:class:`rcpy.led.LED` representing the Robotics Cape *RED* LED.

.. py:data:: green
	     
   :py:class:`rcpy.led.LED` representing the Robotics Cape *GREEN* LED.
       
.. py:data:: ON
	     
   State of an on LED; equal to :py:data:`rcpy.gpio.HIGH`.
	     
.. py:data:: OFF
	     
   State of an off led; equal to :py:data:`rcpy.gpio.LOW`.

Classes
^^^^^^^

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

      Change LED state to :py:data:`rcpy.led.ON`.

   .. py:method:: off()

      Change LED state to :py:data:`rcpy.led.OFF`.
		  
   .. py:method:: toggle()

      Toggle current LED state.
   
   .. py:method:: blink(period)

      :param float period: period of blinking
      :returns: an instance of :py:class:`rcpy.led.Blink`.

      Blinks LED with a period of `period` seconds.
		  
.. py:class:: Blink(led, period)

   :bases: :py:class:`rcpy.clock.Clock`

   :py:class:`rcpy.led.Blink` toggles led on and off periodically.

   :param LED led: the led to toggle
   :param int period: the period in seconds
		  
.. _rcpy_encoder:
   
Module `rcpy.encoder`
---------------------

.. py:module:: rcpy.encoder

This module provides an interface to the four *encoder channels* in
the Robotics Cape. The command::

    import rcpy.encoder as encoder

imports the module. The :ref:`rcpy_encoder` provides objects
corresponding to the each of the encoder channels on the Robotics
Cape, namely :py:data:`rcpy.encoder.encoder1`,
:py:data:`rcpy.encoder.encoder2`, :py:data:`rcpy.encoder.encoder3`,
and :py:data:`rcpy.encoder.encoder4`. It may be convenient to import
one or all of these objects as in::

    from rcpy.encoder import encoder2

The current encoder count can be obtained using::

    encoder2.get()

One can also *reset* the count to zero using::

    encoder2.reset()

or to an arbitrary count using::

    encoder2.set(1024)

after which::

    encoder2.get()

will return 1024.
  
Constants
^^^^^^^^^

.. py:data:: encoder1

   :py:class:`rcpy.encoder.Encoder` representing the Robotics Cape *Encoder 1*.

.. py:data:: encoder2

   :py:class:`rcpy.encoder.Encoder` representing the Robotics Cape *Encoder 2*.
       
.. py:data:: encoder3

   :py:class:`rcpy.encoder.Encoder` representing the Robotics Cape *Encoder 3*.
       
.. py:data:: encoder4

   :py:class:`rcpy.encoder.Encoder` representing the Robotics Cape *Encoder 4*.
	       
Classes
^^^^^^^

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
^^^^^^^^^^^^^^^^^^^

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
-------------------

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

    from rcpy.motor import motor2

This is a convenience object which is equivalent to::

    motor2 = Motor(2)
    
The current average voltage applied to the motor can be set using::

    duty = 1
    motor2.set(duty)

where `duty` is a number varying from -1 to 1 which controls the
percentage of the voltage available to the Robotics Cape that should
be applied on the motor. A motor can be turned off by::

    motor2.set(0)

or using one of the special methods
:py:meth:`rcpy.motor.Motor.free_spin` or
:py:meth:`rcpy.motor.Motor.brake`, which can be used to turn off the
motor and set it in a *free-spin* or *braking* configuration. For
example::

    motor2.free_spin()

puts :py:data:`motor2` in *free-spin* mode. In *free-spin mode* the
motor behaves as if there were no voltage applied to its terminal,
that is it is allowed to spin freely. In *brake mode* the terminals of
the motor are *short-circuited* and the motor winding will exert an
opposing force if the motor shaft is moved. *Brake mode* is
essentially the same as setting the duty cycle to zero.

Constants
^^^^^^^^^

.. py:data:: motor1

   :py:class:`rcpy.motor.Motor` representing the Robotics Cape *Motor 1*.

.. py:data:: motor2

   :py:class:`rcpy.motor.Motor` representing the Robotics Cape *Motor 2*.
       
.. py:data:: motor3

   :py:class:`rcpy.motor.Motor` representing the Robotics Cape *Motor 3*.
       
.. py:data:: motor4

   :py:class:`rcpy.motor.Motor` representing the Robotics Cape *Motor 4*.
	       
Classes
^^^^^^^

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
^^^^^^^^^^^^^^^^^^^

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

.. _rcpy_servo:

Module `rcpy.servo`
-------------------

.. py:module:: rcpy.servo

This module provides an interface to the eight *servo* and *ESC*
(Electronic Speed Control) *channels* in the Robotics Cape. The
3-pin servo connectors are not polarized so make sure the black/brown
ground wire is the one closest to the Robotics Cape. The command::

    import rcpy.servo as servo

imports the module. The :ref:`rcpy_servo` provides objects
corresponding to the each of the servo and ESC channels on the
Robotics Cape, namely :py:data:`rcpy.servo.servo1` through
:py:data:`rcpy.servo.servo8`, and namely :py:data:`rcpy.servo.esc1`
through :py:data:`rcpy.servo.esc8`. It may be convenient to import one
or all of these objects as in ::

    from rcpy.servo import servo7

This is a convenience object which is equivalent to::

    motor7 = Servo(7)
    
The position of the servo can be set using::

    duty = 1.5
    servo7.set(duty)

where `duty` is a number varying from -1.5 to 1.5, which controls the
angle of the servo. This command does not send a pulse to the
servo. In fact, before you can drive servos using the Robotics Cape
you need to enable power to flow to servos using::

    servo.enable()

For safety the servo power rail is disabled by default. Do not enable
the servo power rail when using brushless ESCs as they can be
damaged. Typical brushless ESCs only use the ground and signal pins,
so if you need to control servos and ESC simultaneously simply cut or
disconnect the middle power wire from the ESC connector. Use the
command::

   servo.disable()

to turn off the servo power rail.

Back to servos, you can set the duty *and* send a pulse to the servo
at the same time using the command::

    duty = 1.5
    servo7.pulse(duty)

Alternatively, you can initiate a :py:class:`rcpy.clock.Clock` object
using::

    period = 0.1
    clk = servo7.start(period)

which starts sending the current servor `duty` value to the servo
every 0.1s. The clock can be stopped by::

    clk.stop()

The above is equivalent to::

    import rcpy.clock as clock
    period = 0.1
    clk = clock.Clock(servo7, period)
    clk.start()

Similar commands are available for ESC. For example::
    
    from rcpy.servo import esc3
    duty = 1.0
    esc3.pulse(duty)

sends a *full-throttle* pulse to the ESC in channel 3.

Constants
^^^^^^^^^

.. py:data:: servo1

   :py:class:`rcpy.servo.Servo` representing the Robotics Cape *Servo 1*.

.. py:data:: servo2

   :py:class:`rcpy.servo.Servo` representing the Robotics Cape *Servo 2*.
       
.. py:data:: servo3

   :py:class:`rcpy.servo.Servo` representing the Robotics Cape *Servo 3*.
       
.. py:data:: servo4

   :py:class:`rcpy.servo.Servo` representing the Robotics Cape *Servo 4*.
	       
.. py:data:: servo5

   :py:class:`rcpy.servo.Servo` representing the Robotics Cape *Servo 5*.

.. py:data:: servo6

   :py:class:`rcpy.servo.Servo` representing the Robotics Cape *Servo 6*.

.. py:data:: servo7

   :py:class:`rcpy.servo.Servo` representing the Robotics Cape *Servo 7*.

.. py:data:: servo8

   :py:class:`rcpy.servo.Servo` representing the Robotics Cape *Servo 8*.

.. py:data:: esc1

   :py:class:`rcpy.servo.ESC` representing the Robotics Cape *ESC 1*.

.. py:data:: esc2

   :py:class:`rcpy.servo.ESC` representing the Robotics Cape *ESC 2*.
       
.. py:data:: esc3

   :py:class:`rcpy.servo.ESC` representing the Robotics Cape *ESC 3*.
       
.. py:data:: esc4

   :py:class:`rcpy.servo.ESC` representing the Robotics Cape *ESC 4*.
	       
.. py:data:: esc5

   :py:class:`rcpy.servo.ESC` representing the Robotics Cape *ESC 5*.

.. py:data:: esc6

   :py:class:`rcpy.servo.ESC` representing the Robotics Cape *ESC 6*.

.. py:data:: esc7

   :py:class:`rcpy.servo.ESC` representing the Robotics Cape *ESC 7*.

.. py:data:: esc8

   :py:class:`rcpy.servo.ESC` representing the Robotics Cape *ESC 8*.
       
Classes
^^^^^^^

.. py:class:: Servo(channel, duty = None)

   :param output: servo channel (1 through 4)
   :param state: initial servo duty cycle (Default 0)
	      
   :py:class:`rcpy.servo.Servo` represents servos in the Robotics Cape or Beaglebone Blue.
       
   .. py:method:: set(duty)
            
      Set current servo duty cycle to `duty`. `duty` is a number
      between -1.5 and 1.5. This method does not pulse the servo. Use
      :py:meth:`rcpy.servo.Servo.pulse` for setting *and* pulsing the
      servo at the same time. Otherwise use a
      :py:class:`rcpy.clock.Clock` or the method
      :py:meth:`rcpy.servo.Servo.start` to create one. The value of
      `duty` corresponds to the following pulse widths and servo
      angles:

      .. tabularcolumns:: c|c|c|c
			  
      =====  ======  ======  =================
      input   width  angle   direction
      =====  ======  ======  =================
      -1.5   600us   90 deg  counter-clockwise
      -1.0   900us   60 deg  counter-clockwise
       0.0   1500us  0 deg   neutral
      +1.0   2100us  60 deg  clockwise
      +1.5   2400us  90 deg  clockwise
      =====  ======  ======  =================

   .. py:method:: pulse(duty)
            
      Set current servo duty cycle to `duty` and send a single pulse
      to the servo.

   .. py:method:: run()
            
      Send a single pulse to the servo using the current value of `duty`.
      
   .. py:method:: start(period)

      :param float period: period
      :returns: an instance of :py:class:`rcpy.clock.Clock`.

      Pulses servo periodically every `period` seconds.
      
.. py:class:: ESC(channel, duty = None)

   :param output: ESC channel (1 through 4)
   :param state: initial ESC duty cycle (Default 0)
	      
   :py:class:`rcpy.servo.ESC` represents ESCs in the Robotics Cape
       or Beaglebone Blue.
       
   .. py:method:: set(duty)
            
      Set current ESC duty cycle to `duty`, in which `duty` is a
      number between -0.1 and 1.0. This method does not pulse the
      ESC. Use :py:meth:`rcpy.servo.ESC.pulse` for setting *and*
      pulsing the ESC at the same time. Otherwise use a
      :py:class:`rcpy.clock.Clock` or the method
      :py:meth:`rcpy.servo.ESC.start` to create one. The value of
      `duty` corresponds to the following pulse widths and servo
      angles:

      .. tabularcolumns:: c|c|c|c
			  
      =====  ======  =====  =============
      input   width  power  status
      =====  ======  =====  =============
      -0.1   900us   armed  idle
       0.0   1000us  0%     off
      +0.5   1500us  50%    half-throttle
      +1.0   2000us  100%   full-throttle
      =====  ======  =====  =============
      
   .. py:method:: pulse(duty)
            
      Set current ESC duty cycle to `duty` and send a single pulse to the ESC.

   .. py:method:: run()
            
      Send a single pulses to the ESC using the current value of `duty`.
      
   .. py:method:: start(period)

      :param float period: period
      :returns: an instance of :py:class:`rcpy.clock.Clock`.

      Pulses ESC periodically every `period` seconds.
      
Low-level functions
^^^^^^^^^^^^^^^^^^^

.. py:function:: enable()

   Enables the servo power rail. Be careful when connecting ESCs! 
   
.. py:function:: disable()

   Disables the servo power rail.
   
.. py:function:: pulse(channel, duty)

   :param int channel: servo channel number
   :param int duty: desired servo duty cycle

   Sends a "normalized" pulse to the servo channel `channel`, in
   which `duty` is a float varying from `-1.5` to `1.5`. See
   :py:meth:`rcpy.servo.Servo.set` for details.

   This is a non-blocking call.
		    
.. py:function:: pulse_all(channel, duty)

   :param int duty: desired servo duty cycle

   Sends a "normalized" pulse to all servo channels, in which `duty`
   is a float varying from `-1.5` to `1.5`. See
   :py:meth:`rcpy.servo.Servo.set` for details.

   This is a non-blocking call.
   
.. py:function:: esc_pulse(channel, duty)

   :param int channel: servo channel number
   :param int duty: desired ESC duty cycle

   Sends a "normalized" pulse to the ESC channel `channel`, in
   which `duty` is a float varying from `-0.1` to `1.5`. See
   :py:meth:`rcpy.servo.ESC.set` for details.

   This is a non-blocking call.
		    
.. py:function:: esc_pulse_all(channel, duty)

   :param int duty: desired ESC duty cycle

   Sends a "normalized" pulse to all ESC channels, in which `duty`
   is a float varying from `-0.1` to `1.5`. See
   :py:meth:`rcpy.servo.ESC.set` for details.

   This is a non-blocking call.

.. py:function:: oneshot_pulse(channel, duty)

   :param int channel: ESC channel number
   :param int duty: desired ESC duty cycle

   Sends a "normalized" *oneshot* pulse to the ESC channel
   `channel`, in which `duty` is a float varying from `-0.1` to
   `1.0`.

   This is a non-blocking call.
		    
.. py:function:: oneshot_pulse_all(channel, duty)

   :param int duty: desired ESC duty cycle

   Sends a "normalized" *oneshot* pulse to all ESC channels, in
   which `duty` is a float varying from `-0.1` to `1.0`.

   This is a non-blocking call.
   
.. py:function:: pulse_us(channel, us)

   :param int channel: servo channel number
   :param int us: desired servo duty cycle is :math:`\mu` s

   Sends a pulse of duration `us` :math:`\mu` s to all servo channels. 
   This is a non-blocking call.

   This is a non-blocking call.
		    
.. py:function:: pulse_us_all(channel, us)

   :param int us: desired servo duty cycle is :math:`\mu` s

   Sends a pulse of duration `us` :math:`\mu` s to all servo channels.
   This is a non-blocking call.
   
.. _rcpy_mpu9250:

Module `rcpy.mpu9250`
---------------------

.. py:module:: rcpy.mpu9250

This module provides an interface to the on-board `MPU-9250
<https://www.invensense.com/products/motion-tracking/9-axis/mpu-9250/>`_
Nine-Axis (Gyro + Accelerometer + Compass) MEMS device. The command::

    import rcpy.mpu9250 as mpu9250

imports the module.

**IMPORTANT:** Beware that due to the way the Robotics Cape is written
objects of the class :py:class:`rcpy.mpu9250.IMU` are singletons, that
is they all refer to the same instance. 

Setup can be done at creation, such as in ::

    imu = mpu9250.IMU(enable_dmp = True, dmp_sample_rate = 4,
                      enable_magnetometer = True)

which starts and initializes the MPU-9250 to use its DMP (Dynamic
Motion Processor) to provide periodic readings at a rate of 4 Hz and
also its magnetometer.

The data can be read using::

    imu.read()

which performs a blocking call and can be used to synchronize
execution with the DMP. For example::

    while True:
        data = imu.read()
	print('heading = {}'.format(data['head']))

will print the current heading at a rate of 4 Hz. More details about
the configuration options and the format of the data can be obtained
in the help for the functions :py:func:`rcpy.mpu9250.initialize` and
:py:func:`rcpy.mpu9250.read`.

Constants
^^^^^^^^^

The following constants can be used to set the accelerometer full scale register:
       
.. py:data:: ACCEL_FSR_2G
.. py:data:: ACCEL_FSR_4G
.. py:data:: ACCEL_FSR_8G
.. py:data:: ACCEL_FSR_16G

The following constants can be used to set the gyroscope full scale register:

.. py:data:: GYRO_FSR_250DPS
.. py:data:: GYRO_FSR_500DPS
.. py:data:: GYRO_FSR_1000DPS
.. py:data:: GYRO_FSR_2000DPS

The following constants can be used to set the accelerometer low-pass filter:
   
.. py:data:: ACCEL_DLPF_OFF
.. py:data:: ACCEL_DLPF_184
.. py:data:: ACCEL_DLPF_92
.. py:data:: ACCEL_DLPF_41
.. py:data:: ACCEL_DLPF_20
.. py:data:: ACCEL_DLPF_10
.. py:data:: ACCEL_DLPF_5

The following constants can be used to set the gyroscope low-pass filter:
	     
.. py:data:: GYRO_DLPF_OFF
.. py:data:: GYRO_DLPF_184
.. py:data:: GYRO_DLPF_92
.. py:data:: GYRO_DLPF_41
.. py:data:: GYRO_DLPF_20
.. py:data:: GYRO_DLPF_10
.. py:data:: GYRO_DLPF_5

The following constants can be used to set the imu orientation:
   
.. py:data:: ORIENTATION_Z_UP
.. py:data:: ORIENTATION_Z_DOWN
.. py:data:: ORIENTATION_X_UP
.. py:data:: ORIENTATION_X_DOWN
.. py:data:: ORIENTATION_Y_UP
.. py:data:: ORIENTATION_Y_DOWN
.. py:data:: ORIENTATION_X_FORWARD
.. py:data:: ORIENTATION_X_BACK
       
Classes
^^^^^^^

.. py:class:: IMU(**kwargs)

   :param kwargs kwargs: keyword arguments
	      
   :py:class:`rcpy.mpu9250.imu` represents the MPU-9250 in the Robotics Cape or Beaglebone Blue.

   Any keyword accepted by :py:func:`rcpy.mpu9250.initialize` can be given.
       
   .. py:method:: set(**kwargs)
            
      :param kwargs kwargs: keyword arguments
			 
      Set current MPU-9250 parameters.

      Any keyword accepted by :py:func:`rcpy.mpu9250.initialize` can be given.
      
   .. py:method:: read()
            
      :returns: dictionary with current MPU-9250 measurements

      Dictionary is constructed as in :py:func:`rcpy.mpu9250.read`.

Low-level functions
^^^^^^^^^^^^^^^^^^^

.. py:function:: initialize(accel_fsr, gyro_fsr, accel_dlpf, gyro_dlpf, enable_magnetometer, orientation, compass_time_constant, dmp_interrupt_priority, dmp_sample_rate, show_warnings, enable_dmp, enable_fusion)

   :param int accel_fsr: accelerometer full scale
   :param int gyro_fsr: gyroscope full scale
   :param int accel_dlpf: accelerometer low-pass filter
   :param int gyro_dlpf: gyroscope low-pass filter
   :param bool enable_magnetometer: :py:data:`True` enables the magnetometer
   :param int orientation: imu orientation
   :param float compass_time_constant: compass time-constant
   :param int dmp_interrupt_priority: DMP interrupt priority
   :param int dmp_sample_rate: DMP sample rate
   :param int show_warnings: :py:data:`True` shows warnings
   :param bool enable_dmp: :py:data:`True` enables the DMP
   :param bool enable_fusion: :py:data:`True` enables data fusion algorithm

   Configure and initialize the MPU-9250.

   All parameters are optional. Default values are obtained by calling
   the :c:func:`rc_get_default_imu_config` from the Robotics Cape
   library.
   
.. py:function:: power_off()

   Powers off the MPU-9250
		 
.. py:function:: read_accel_data()

   :returns: list with three-axis acceleration in m/s :math:`\!^2`

   This function forces the MPU-9250 registers to be read.
	     
.. py:function:: read_gyro_data()

   :returns: list with three-axis angular velocities in deg/s
	     
   This function forces the MPU-9250 registers to be read.
   
.. py:function:: read_mag_data()

   :raises mup9250Error: if magnetometer is disabled
			 
   :returns: list with 3D magnetic field vector in :math:`\mu\!` T
   
   This function forces the MPU-9250 registers to be read.
   
.. py:function:: read_imu_temp()

   :returns: the imu temperature in deg C

   This function forces the MPU-9250 registers to be read.
   
.. py:function:: read()

   :returns: dictionary with the imu data; the keys in the dictionary depend on the current configuration
	     
   If the magnetometer is *enabled* the dictionary contains the
   following keys:
   
   * **accel**: 3-axis accelerations (m/s :math:`\!^2`)
   * **gyro**: 3-axis angular velocities (degree/s)
   * **mag**: 3D magnetic field vector in (:math:`\mu\!` T)
   * **quat**: orientation quaternion 
   * **tb**: pitch/roll/yaw X/Y/Z angles (radians)
   * **head**: heading from magnetometer (radians)

   If the magnetometer is *not enabled* the keys **mag** and **head**
   are not present.

   This function forces the MPU-9250 registers to be read only if the
   DMP is disabled. Otherwise it returns the latest DMP data. It is a
   blocking call.
