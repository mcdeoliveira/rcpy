import rcpy
import rcpy.gpio as gpio

#gpio.export(gpio.RED_LED)
gpio.set_dir(gpio.RED_LED, gpio.OUT)
gpio.set_value(gpio.RED_LED, gpio.ON)

