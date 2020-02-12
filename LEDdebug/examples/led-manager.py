#!/usr/bin/env python3
"""UrsaLeo LEDdebug board LED manager
   Monitor system processes using LED flags"""

import time
import os
import argparse

ON = 1
OFF = 0
DELAY = 0.5  # seconds

try:
    from LEDdebug import LEDdebug
except ImportError:
    try:
        import sys
        sys.path.append("..")
        sys.path.append(os.path.join(os.path.dirname(__file__), '..',
                        'LEDdebug'))
        from LEDdebug import LEDdebug
    except ImportError:
        print('LEDdebug import failed')
        exit(0)


def parse_command_line_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--service1',
                        default='/tmp/LED1',
                        help='Service 1 monitor on LED1')
    parser.add_argument('--service2',
                        default='/tmp/LED2',
                        help='Service 2 monitor on LED2')
    return parser.parse_args()

def manage_led_blink(device, led, flag):
    """Solid LED if flag is found, blink if not"""
    if os.path.exists(flag):
        device.set_led(led, ON)
    else:
        device.set_led(led, not device.get_led_state(led))


def manage_led_solid(device, led, flag):
    """Solid LED if found, off if not"""
    if os.path.exists(flag):
        device.set_led(led, ON)
    else:
        device.set_led(led, OFF)


def is_service1_running(device, flag):
    """Monitor network connection on LED1"""
    manage_led_blink(device, 1, flag)


def is_service2_running(device, flag):
    """Monitor sensor connection on LED2"""
    manage_led_blink(device, 2, flag)


device = LEDdebug()


def main():
    args = parse_command_line_args()
    try:
        while True:
            is_service1_running(device, args.service1)
            is_service2_running(device, args.service2)
            time.sleep(DELAY)

    finally:
        device.set_leds(OFF)


if __name__ == '__main__':
    main()
