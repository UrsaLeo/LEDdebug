#!/usr/bin/env python3
"""UrsaLeo LEDdebug board button demo
   Capture button presses using interrupts to turn on LED's
   Press CTR+C to exit"""

import time

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


def main():
    # Create device
    device = LEDdebug()

    while True:
        try:
            button = device.get_button()
            if button:  # Button SW1 or SW2 pressed
                time.sleep(0.5)  # Debounce
                #Toggle LEDs when buttons are pressed
                if button == 1:  # Button 1
                    device.set_led(1, not device.get_led_state(1))
                else:  # Button 2
                    device.set_led(2, not device.get_led_state(2))
                print(f'Button {button} pressed')
        except KeyboardInterrupt:
            # Turn the lights off when leaving!
            device.set_leds(0)
            exit(0)


if __name__ == '__main__':
    main()
