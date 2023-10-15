# SPDX-FileCopyrightText: Copyright (c) 2023 Tod Kurt
#
# SPDX-License-Identifier: MIT
"""
`ruhrohrotaryio`
================================================================================

Pretend to be 'rotaryio' for boards that need non-sequential pins


* Author(s): Tod Kurt / @todbot

Implementation Notes
--------------------

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads

"""

# imports

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/todbot/CircuitPython_RuhRohRotaryIO.git"


import keypad
from digitalio import DigitalInOut, Direction, Pull


class IncrementalEncoder:
    """A simple drop-in replacement for rotaryio.IncrementalEncoder that works
    on non-sequential pins on RP2040"""

    def __init__(self, pin_a, pin_b, divisor=4):  # divisor is unused currently
        pin = DigitalInOut(pin_a)
        pin.switch_to_input(pull=Pull.UP)
        self._key1_val = pin.value  # get initial pin state
        pin.deinit()  # just needed it to check pin state
        self._encoder_keys = keypad.Keys(
            (pin_a, pin_b), value_when_pressed=False, pull=True
        )
        self._position = 0
        self._update()  # do an initial read
        self._position = 0  # and then zero it out

    def _update(self):
        while key := self._encoder_keys.events.get():
            if key.key_number == 0:
                if key.pressed:
                    if self._key1_val:
                        self._position -= 1
                    else:
                        self._position += 1
                else:
                    if self._key1_val:
                        self._position += 1
                    else:
                        self._position -= 1

            if key.key_number == 1:
                self._key1_val = key.pressed

    @property
    def position(self):
        self._update()
        return self._position

    @position.setter
    def position(self, value):
        self._position = value
