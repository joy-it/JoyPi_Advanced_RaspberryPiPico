import utime

class I2CLCD:
    
    def __init__(self, i2c, addr = 0x21):
        """
        i2c - i2c port
        addr - adress of MCP23008
        """
        self._addr = addr
        self.i2c = i2c
        
        self.i2c.writeto(self._addr, bytes([0x00, 0x00]))
        self.backlight = 0x80
        self.registerSelect = 0x02
        self.en = 0x04
        
        self.columns = 16
        self.rows = 2
        
        
    def _write(self, data):
        """
        making a write operation
        """
        self.i2c.writeto(self._addr, bytes([0x09, data | self.en]))
        utime.sleep_us(1)
        self.i2c.writeto(self._addr, bytes([0x09, data & ~self.en]))
        utime.sleep_us(50)
        
        
    def _set(self, data, is_data):
        """
        preparing data for write operation
        """
        _data = ((data & 0x0F) << 3)
        if is_data:
            _data |= self.registerSelect
        _data |= self.backlight
        self._write(_data)
    
    def _send(self, data, is_data):
        """
        splitting data in two parts
        """
        self._set(data >> 4, is_data)
        self._set(data & 0x0F, is_data)
    
    def _command(self, data):
        """
        making a command operation
        """
        self._send(data, is_data=False)
        
        
    def _sendData(self, data):
        """
        making a send data operation
        """
        self._send(data, is_data=True)
        
    
    def begin(self):
        """
        setup communciation with LCD
        """
        utime.sleep_ms(50)
        
        for i in range(3):
            self._set(0x03, False)
            utime.sleep_ms(5)
        self._set(0x02, False)

        self._command(0x28)
        self._command(0x08)
        self._command(0x01)
        utime.sleep_ms(2)
        self._command(0x06)
        self._command(0x0C) 
    
    
    def clear(self):
        """
        clear LCD
        """
        self._command(0x01)
        utime.sleep_ms(2)
    
    
    def setHome(self):
        """
        set cursor to (0,0)
        """
        self.setCursor(0,0)
        
    
    def shiftToLeft(self):
        """
        shift display to the left
        """
        self._command(0x18)
    
    
    def shiftToRight(self):
        """
        shift display to the right
        """
        self._command(0x1C)
    
    
    def showCursor(self):
        """
        show cursor
        """
        self._command(0x0E)
    
    
    def blinkingCursor(self):
        """
        activate blinking cursor
        """
        self._command(0x0F)
    
    
    def hideCursor(self):
        """
        hide cursor
        """
        utime.sleep(1)
        self._command(0x0C)
    
    
    def turnOff(self):
        """
        turn off LCD
        """
        self.backlight = 0x00
        self._command(0x00)

    
    def turnOn(self):
        """
        turn on LCD
        """
        self.backlight = 0x80
        self._command(0x04)


    def setCursor(self, x, y):
        """
        set cursor to position (x,y)
        """
        pos = 0
        if y > self.rows : y = self.rows - 1
        if x > self.columns: x = self.columns -1
        
        if y > 0: pos = 0xC0
        else: pos = 0x80
        utime.sleep_ms(1)
        pos += x
        self._command(pos)


    def print(self, text):
        """
        print on LCD LCD
        """
        for char in text:
            self._sendData(ord(char))
