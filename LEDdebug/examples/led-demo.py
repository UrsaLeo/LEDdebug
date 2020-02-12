#!/usr/bin/env python3
"""UrsaLeo LEDdebug board LED demo
   Turn the LED's on one at a time, then all off"""

import time

ON = 1
OFF = 0
DELAY = 0.5  # seconds

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

    # Turn on each LED in succession
    for led in range(1, 7):
        device.set_led(led, ON)
        print(f'Turning LED{led} on')
        time.sleep(DELAY)

    print('Turning all LEDs off')
    # Turn all the lights of before leaving!
    device.set_leds(OFF)


if __name__ == '__main__':
    main()
