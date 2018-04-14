#!/usr/bin/env python3

# Contributed by BrendanSimon

# import rcpy libraries
import rcpy
import rcpy.adc as adc

def adc_test():
    # Read ADC channels via function calls.
    for ch in range(adc.CHANNEL_COUNT):
        raw = adc.get_raw(ch)
        voltage = adc.get_voltage(ch)
        print("channel={} : raw={:4} voltage={:+6.2f}".format(ch, raw, voltage))

    # Read ADC channels via class instances.
    for ch, a in enumerate(adc.adc):
        raw = a.get_raw()
        voltage = a.get_voltage()
        print("adc[{}] : raw={:4} voltage={:+6.2f}".format(ch, raw, voltage))

    # Read DC Jack and Battery voltages via function calls.
    dc_jack_voltage = adc.get_dc_jack_voltage()
    battery_voltage = adc.get_battery_voltage()
    print("dc-jack : voltage={:+6.2f}".format(dc_jack_voltage))
    print("battery : voltage={:+6.2f}".format(battery_voltage))
    
    # Read DC Jack and Battery voltages via class instances.
    dc_jack_voltage = adc.dc_jack.get_voltage()
    battery_voltage = adc.battery.get_voltage()
    print("dc-jack : voltage={:+6.2f}".format(dc_jack_voltage))
    print("battery : voltage={:+6.2f}".format(battery_voltage))
        
if __name__ == "__main__":
    adc_test()

