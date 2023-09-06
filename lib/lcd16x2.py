import utime

class I2CLCD:
    
    def __init__(self, i2c, addr = 0x21):
        """
        i2c - i2c port
        addr - adress of MCP23008
        """
        self._addr = addr
        self.i2c = i2c
        self.backlight = 0x80
        self.registerSelect = 0x00
        self.columns = 16
        self.rows = 2
        
        
    def _write(self, data):
        """
        making a write operation
        """
        self.i2c.writeto(self._addr, bytes([0x09, data|0x04, data]))
        
        
    def _set(self, data):
        """
        making a set operation
        """
        temp = (data & 0xF0) >> 1
        temp = temp | self.backlight | self.registerSelect
        self._write(temp)
    
    
    def _command(self, data):
        """
        making a command operation
        """
        self.registerSelect = 0x00
        self._set(data)
        self._set(data << 4)
        
        
    def _sendData(self, data):
        """
        making a send data operation
        """
        self.registerSelect = 0x02
        self._set(data)
        self._set(data << 4)
        
    
    def begin(self):
        """
        setup communciation with LCD
        """
        self.i2c.writeto(self._addr, bytes([0x00, 0xFF]))
        self.i2c.writeto(self._addr, bytes([0x06, 0x00]))
        self.i2c.writeto(self._addr, bytes([0x00, 0xFD]))
        self.i2c.writeto(self._addr, bytes([0x00, 0xF9]))
        self.i2c.writeto(self._addr, bytes([0x00, 0xF1]))
        self.i2c.writeto(self._addr, bytes([0x00, 0xE1]))
        self.i2c.writeto(self._addr, bytes([0x00, 0xC1]))
        self.i2c.writeto(self._addr, bytes([0x00, 0x81]))
        self.i2c.writeto(self._addr, bytes([0x00, 0x01]))
        self.i2c.writeto(self._addr, bytes([0x09, 0x00]))
    
        utime.sleep_ms(1)
        
        self._command(0x33)
        self._command(0x32)
        self._command(0x0C)
        self._command(0x28)
        self._command(0x06)
        
        self.clear()
        self.setHome()
    
    
    def clear(self):
        """
        clear LCD
        """
        self._command(0x01)
    
    
    def setHome(self):
        """
        set cursor to (0,0)
        """
        self._command(0x02)
    
    
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
        self._set(0)
        self._command(0x00)

    
    def turnOn(self):
        """
        turn on LCD
        """
        self.backlight = 0x80
        self._set(0)
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
        utime.sleep_ms(3)
        for i in range(len(text)):
            self._sendData(ord(text[i]))
            utime.sleep_ms(10)


