#!/usr/bin/env python3
"""UrsaLeo LEDdebug threaded button demo
   Toggle LED6 while capturing button presses on SW1 & SW2
   Press CTR+C to exit"""

import time
import threading

try:
    from LEDdebug import LEDdebug
except ImportError:
    try:
        import sys
        import os
        sys.path.append("..")
        sys.path.append(os.path.join(os.path.dirname(__file__), '..',
                        'LEDdebug'))
        from LEDdebug import LEDdebug
    except ImportError:
        print('LEDdebug import failed')
        exit(0)


def button_pressed(device, button):
    """ Callback function
        Toggle LEDs when buttons are pressed"""
    if button == 1:  # Button 1
        device.set_led(1, not device.get_led_state(1))
    else:  # Button 2
        device.set_led(2, not device.get_led_state(2))


def interrupt(device):
    """ Interrupt function
        Trigger callback function if SW1 or SW2 are pressed"""
    while True:
        button = device.get_button()
        if button:  # Button SW1 or SW2 pressed
            time.sleep(0.5)  # Debounce
            button_pressed(device, button)


def main():
    # Create device
    device = LEDdebug()

    # Detect button presses in background
    timer = threading.Thread(target=interrupt, args=[device])
    timer.daemon = True
    timer.start()

    while True:
        try:
            # Toggle LED6 in forground
            # Other processes can run here
            device.set_led(6, not device.get_led_state(6))
            time.sleep(1)
        except KeyboardInterrupt:
            # Turn the lights off when leaving!
            device.set_leds(0)
            exit(0)


if __name__ == '__main__':
    main()
