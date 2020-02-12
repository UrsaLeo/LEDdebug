# Copyright 2020 URSALEO, Inc.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

""" UrsaLeo LEDdebug board library
    Requires python smbus
    LED1-6, SW1 & SW2 are programable
    SW3 triggers poweroff
    """

from smbus import SMBus
import time

I2C_ADDR = 0x20
I2C_BUS = 1
GPIO_ADDR = 0x09
GPPU_ADDR = 0x06
IODIR_ADDR = 0x00
OLAT_ADDR = 0x0a
GPINTEN_ADDR = 0x02
DEFVAL_ADDR = 0x03
INTCON_ADDR = 0x04
INTF_ADDR = 0x07

ON = 1
OFF = 0

LED1 = 1  # GP0
LED2 = 2  # GP1
LED3 = 3  # GP2
LED4 = 4  # GP3
LED5 = 5  # GP4
LED6 = 6  # GP5

SW1 = 1  # GP6
SW2 = 2  # GP7


class LEDdebug:
    """LEDdebug class
       Default I2C bus 1 at address 0x20"""

    def __init__(self, bus=I2C_BUS, address=I2C_ADDR):
        self.i2c_addr = address
        self.i2c_bus = bus  # Bus number
        self.bus = self.get_bus()  # Bus object
        self.get_gpio()  # Check board is installed
        self.set_pullups(0xc0)
        self.set_outputs(0xc0)  # Set GP0-5 as outputs (LED1-6)
        self.set_leds(OFF)
        self.enable_buttons()  # Enable interrups on GP6-7 (SW1 & SW2)
        self.flash()
        print('LEDdebug installed bus: {0} addr: {1}'.format(self.i2c_bus,
              hex(self.i2c_addr)))

    def set_bit(self, byte, bit, value) -> 'byte':
        """Set individual bit within byte - inverted logic!"""
        try:
            if value == 1:
                return byte & ~(1 << bit)
            elif value == 0:
                return byte | (1 << bit)
        except ValueError:
            print('Pin value error')
            exit(0)

    def get_bit(self, byte, bit) -> 'bit':
        """Get individual bit within a byte"""
        value = 0
        if byte & (1 << bit):
            value = 1
        return value

    def get_bus(self) -> 'bus':
        """ Get the I2C bus object
            Exits successfully if bus is not configured"""
        try:
            return SMBus(self.i2c_bus)
        except IOError:
            print('Could not open I2C bus', self.i2c_bus)
            exit(0)

    def get_gpio(self) -> 'byte':
        """ Get the GPIO register values
            Exits successfully if board is not installed"""
        try:
            return self.bus.read_byte_data(self.i2c_addr, GPIO_ADDR)
        except IOError:
            print('LEDdebug not found at addr', hex(self.i2c_addr))
            exit(0)

    def set_outputs(self, value):
        """Set pins as pullups"""
        self.bus.write_byte_data(self.i2c_addr, GPPU_ADDR, value)

    def set_pullups(self, value):
        """Set pins as outputs"""
        self.bus.write_byte_data(self.i2c_addr, IODIR_ADDR, value)

    def set_leds(self, status):
        """Turn all LED pins (GP0-5) ON or OFF"""
        if status == ON:
            self.bus.write_byte_data(self.i2c_addr, OLAT_ADDR, 0xc0)
        else:
            self.bus.write_byte_data(self.i2c_addr, OLAT_ADDR, 0x3f)

    def set_led(self, led, status):
        """ Turn individual LED pin ON or OFF
            Exits successfully if board is not installed"""
        if led in (LED1, LED2, LED3, LED4, LED5, LED6):
            pin = led - 1
            # Get the current value of outputs
            byte = self.set_bit(self.get_gpio(), pin, status)
            # Update outputs to new value
            self.bus.write_byte_data(self.i2c_addr, OLAT_ADDR, byte)
        else:
            print('Invalid LED value', led)
            exit(0)

    def flash(self):
        """Flash all LED's"""
        for led in (ON, OFF):
            self.set_leds(led)
            time.sleep(0.5)

    def enable_buttons(self):
        """Set GP6-7 (SW1 & SW2) as interrupts"""
        # Enable GPIO input pin for interrupt-on-change event
        self.bus.write_byte_data(self.i2c_addr, GPINTEN_ADDR, 0xc0)
        # Enable comparison with DEFVAL value
        self.bus.write_byte_data(self.i2c_addr, DEFVAL_ADDR, 0xc0)
        # Compare interrupt pin with DEFVAL
        self.bus.write_byte_data(self.i2c_addr, INTCON_ADDR, 0xc0)
        # Clear interrupts
        self.get_gpio()

    def get_button(self) -> 'button':
        """ Get the button pressed
            Interrupt must be cleared by reading GPIO
            after calling this function"""
        # Read INTF byte when interrupt occured
        byte = self.bus.read_byte_data(self.i2c_addr, INTF_ADDR)
        if self.get_button_state(byte, 1):
            return SW1
        if self.get_button_state(byte, 2):
            return SW2

    def get_button_state(self, byte, button) -> 'bit':
        """ Get buttons status when interrupt triggered
            Returns 1 (pressed) / 0 (not pressed)"""
        if button in (SW1, SW2):
            pin = button + 5
            return self.get_bit(byte, pin)
        else:
            print('Invalid button value', button)
            exit(0)

    def get_led_state(self, led) -> 'ON/OFF':
        """ Get LED status
            Returns 1 (ON) / 0 (OFF) - inverts logic
            Will clear INTF when called after get_button"""
        if led in (LED1, LED2, LED3, LED4, LED5, LED6):
            pin = led - 1
            # Read GPIO byte when interrupt occured
            byte = self.bus.read_byte_data(self.i2c_addr, GPIO_ADDR)
            value = OFF
            if self.get_bit(byte, pin):
                value = ON
            return not value
        else:
            print('Invalid LED value', led)
            exit(0)


def main():
    device = LEDdebug()
    for led in (LED1, LED2, LED3, LED4, LED5, LED6):
        device.set_led(led, ON)
        print('GPIO:', hex(device.get_gpio()))
        time.sleep(0.5)
    device.set_leds(OFF)


if __name__ == '__main__':
    main()
