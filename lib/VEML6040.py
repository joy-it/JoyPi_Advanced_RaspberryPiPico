"""
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

    CONF_REG = 0x00
    RED_REG = 0x08
    GREEN_REG = 0x09
    BLUE_REG = 0x0A
    WHITE_REG = 0x0B

    def __init__(self, i2c, address=0x10):
        """
        initialize colour sensor
        i2c - established i2c connection
        address - i2c addresss of color sensor
        """
        self.i2c = i2c
        self.address = address
        self.enableSensor()


    def _write_register(self, reg, value):
        """
        write value into register on the colour sensor
        reg - register
        value - value to be written
        """
        self.i2c.writeto_mem(self.address, reg, bytearray([value]))
        

    def _read_register(self, reg):
        """
        read value from register on the colour sensor
        reg - register
        """
        return int.from_bytes(self.i2c.readfrom_mem(self.address, reg, 2), 'little')


    def enableSensor(self):
        """
        activate sensor
        """
        conf = self._read_register(self.CONF_REG) & 0x00FE
        self._write_register(self.CONF_REG, conf)
        
        
    def disableSensor(self):
        """
        deactivate sensor
        """
        conf = (self._read_register(self.CONF_REG) & 0x00FE) | 0x00
        self._write_register(self.CONF_REG, conf)
        utime.sleep_ms(1)
        
        
    def setIntegrationTime(self, int_time):
        """
        set integration time with variable int_time
        int_time - integration time 
            0 = 40 ms
            1 = 80 ms
            2 = 160 ms
            3 = 320 ms
            4 = 640 ms
            5 = 1280 ms
        """
        if int_time < 0 or int_time > 5:
            raise ValueError('int_time is not in range')
        conf = self._read_register(self.CONF_REG) & 0x0003
        self._write_register(self.CONF_REG, (conf | (int_time << 4)))
        
    
    def forceMode(self):
        """
        forces measurement mode - triggers to start
        """
        conf = (self._read_register(self.CONF_REG) & 0x0072) | 0x0002
        self._write_register(self.CONF_REG, conf)
        
        
    def autoMode(self):
        """
        automatic measurement mode
        """
        conf = self._read_register(self.CONF_REG) & 0x0070
        self._write_register(self.CONF_REG, conf)
        
        
    def get_red(self):
        """
        returns raw value of red
        """
        return self._read_register(self.RED_REG)
    

    def get_green(self):
        """
        returns raw value of green
        """
        return self._read_register(self.GREEN_REG)
    

    def get_blue(self):
        """
        returns raw value of blue
        """
        return self._read_register(self.BLUE_REG)
    

    def get_white(self):
        """
        returns raw value of white
        """
        return self._read_register(self.WHITE_REG)
    

    def get_rgbw(self):
        """
        returns raw value of all RGBW values
        """
        return self.get_red(), self.get_green(), self.get_blue(), self.get_white()


    def readAll(self):
        """
        returns most recognized colour and raw values
        """
        r, g, b, w = self.get_rgbw()
        raw_val = [r, g, b, w]
        dominant_col, dominant_val = "red", r
        if b > dominant_val: dominant_col, dominant_val = "blue", b
        if g > dominant_val: dominant_col, dominant_val = "green", g
        return dominant_col, raw_val