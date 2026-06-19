"""
###################################################################################
# Edited by Joy-IT
###################################################################################
Author: Core Electronics Pty Ltd.
https://github.com/CoreElectronics/CE-PiicoDev-VEML6040-MicroPython-Module/tree/main

The MIT License (MIT)

Copyright (c) 2020 Core Electronics Pty Ltd.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import utime

class VEML6040:

    REG_CONF = 0x00
    REG_RED = 0x08
    REG_GREEN = 0x09
    REG_BLUE = 0x0A
    REG_WHITE = 0x0B
    
    INTEGRATION_TIME_40MS = 0
    INTEGRATION_TIME_80MS = 1
    INTEGRATION_TIME_160MS = 2
    INTEGRATION_TIME_320MS = 3
    INTEGRATION_TIME_640MS = 4
    INTEGRATION_TIME_1280MS = 5

    _INTEGRATION_TIME_VALUES = {
        INTEGRATION_TIME_40MS: 0x00,
        INTEGRATION_TIME_80MS: 0x10,
        INTEGRATION_TIME_160MS: 0x20,
        INTEGRATION_TIME_320MS: 0x30,
        INTEGRATION_TIME_640MS: 0x40,
        INTEGRATION_TIME_1280MS: 0x50,
    }

    _INTEGRATION_TIME_DELAY = {
        INTEGRATION_TIME_40MS: 40,
        INTEGRATION_TIME_80MS: 80,
        INTEGRATION_TIME_160MS: 160,
        INTEGRATION_TIME_320MS: 320,
        INTEGRATION_TIME_640MS: 640,
        INTEGRATION_TIME_1280MS: 1280,
    }

    BIT_SD = 0x01
    BIT_AF = 0x02
    BIT_TRIG = 0x04
    MASK_INTEGRATION_TIME = 0x70

    def __init__(self, i2c, integration_time=INTEGRATION_TIME_160MS, address=0x10):
        """
        initialize colour sensor
        i2c - established i2c connection
        integration_time - 
        address - i2c addresss of color sensor
        """
        if integration_time not in self._INTEGRATION_TIME_VALUES:
            raise ValueError("integration_time is not in range")
        self.integration_time = integration_time
        self.i2c = i2c
        self.address = address
        self.enableSensor()


    def _write_register(self, reg, value):
        """
        write value into register on the colour sensor
        reg - register
        value - value to be written
        """
        data = bytes([
            reg & 0xFF,
            value & 0xFF,
            (value >> 8) & 0xFF,
        ])
        
        self.i2c.writeto_mem(self.address, reg, data)
        

    def _read_register(self, reg):
        """
        read value from register on the colour sensor
        reg - register
        """
        register = bytes([reg & 0xFF])
        last_error = None
        
        for _ in range(3):
            try:
                return int.from_bytes(self.i2c.readfrom_mem(self.address, reg, 2), 'little')
            except OSError as error:
                last_error = error
                utime.sleep_ms(20)
        raise last_error


    def enableSensor(self):
        """
        activate sensor
        """
        config = self._INTEGRATION_TIME_VALUES[self.integration_time]
        config &= ~self.BIT_SD
        config &= ~self.BIT_AF
        config &= ~self.BIT_TRIG
        self._write_register(self.REG_CONF, config)
        utime.sleep_ms(self._INTEGRATION_TIME_DELAY[self.integration_time])
        
        
    def disableSensor(self):
        """
        deactivate sensor
        """
        config = self._read_register(self.REG_CONF)
        config |= self.BIT_SD
        self._write_register(self.REG_CONF, config)
        
        
    def setIntegrationTime(self, integration_time):
        """
        set integration time with variable integration_time
        integration_time - _INTEGRATION_TIME_VALUES 
            INTEGRATION_TIME_40MS = 40 ms
            INTEGRATION_TIME_80MS = 80 ms
            INTEGRATION_TIME_160MS = 160 ms
            INTEGRATION_TIME_320MS = 320 ms
            INTEGRATION_TIME_640MS = 640 ms
            INTEGRATION_TIME_1280MS = 1280 ms
        """
        if integration_time not in self._INTEGRATION_TIME_VALUES:
            raise ValueError("integration_time is not in range")
        config = self._read_register(self.REG_CONF)
        config &= ~self.MASK_INTEGRATION_TIME
        config |= self._INTEGRATION_TIME_VALUES[integration_time]
        config &= ~self.BIT_SD
        self.integration_time = integration_time
        self._write_register(self.REG_CONF, config)
        utime.sleep_ms(self._INTEGRATION_TIME_DELAY[self.integration_time])
        
    
    def forceMode(self):
        """
        forces measurement mode - triggers to start
        """
        config = self._read_register(self.REG_CONF)
        config &= self.MASK_INTEGRATION_TIME
        config |= self.BIT_AF
        config |= self.BIT_TRIG
        config &= ~self.BIT_SD
        self._write_register(self.REG_CONF, config)
        utime.sleep_ms(self._INTEGRATION_TIME_DELAY[self.integration_time])
        
        
    def autoMode(self):
        """
        automatic measurement mode
        """
        config = self._read_register(self.REG_CONF)
        config &= self.MASK_INTEGRATION_TIME
        config &= ~self.BIT_AF
        config &= ~self.BIT_TRIG
        config &= ~self.BIT_SD
        self._write_register(self.REG_CONF, config)
        utime.sleep_ms(self._INTEGRATION_TIME_DELAY[self.integration_time])
        
        
    def get_red(self):
        """
        returns raw value of red
        """
        return self._read_register(self.REG_RED)
    

    def get_green(self):
        """
        returns raw value of green
        """
        return self._read_register(self.REG_GREEN)
    

    def get_blue(self):
        """
        returns raw value of blue
        """
        return self._read_register(self.REG_BLUE)
    

    def get_white(self):
        """
        returns raw value of white
        """
        return self._read_register(self.REG_WHITE)
    

    def get_rgbw(self):
        """
        returns raw value of all RGBW values
        """
        red = self.get_red()
        utime.sleep_ms(5)
        green = self.get_green()
        utime.sleep_ms(5)
        blue = self.get_blue()
        utime.sleep_ms(5)
        white = self.get_white()
        return red, green, blue, white


    def readAll(self):
        """
        returns most recognized colour and raw values
        """
        red, green, blue, white = self.get_rgbw()
        values = {
            "red": red,
            "green": green,
            "blue": blue,
        }

        dominant_color = max(values, key=values.get)
        return dominant_color, [red, green, blue, white]