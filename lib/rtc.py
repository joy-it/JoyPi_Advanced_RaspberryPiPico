import utime

class DS1307Z:
    
    RTCSECOND = 0x00
    RTCMINUTE = 0x01
    RTCHOUR = 0x02
    RTCWEEKDAY = 0x03
    RTCDAY = 0x04
    RTCMONTH = 0x05
    RTCYEAR = 0x06
    RTCCTRL = 0x07
    RTCRAM = 0x08
    
    month = ["January", "February", "March", "April", "May", "June",
             "July", "August", "September", "October", "November", "December"]
    weekday = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    
    def __init__(self, i2c, addr = 0x68):
        """
        i2c - i2c port
        addr - adress of MCP23008
        """
        self._addr = addr
        self.i2c = i2c
        
        
    def _writeReg(self, reg, data):
        """
        write data in register
        """
        self.i2c.writeto_mem(self._addr, reg, bytes([data]))
    
    
    def _readReg(self, reg):
        """
        read data from register
        """
        return self.i2c.readfrom_mem(self._addr, reg, 1)[0]
    
    
    def _hexToDec(self, hex):
        """
        convert from hex to decimal
        """
        return (hex >> 4) * 10 + (hex % 16)
    
    
    def _decToHex(self, dec):
        """
        convert from decimal to hex
        """
        return (dec // 10) * 16 + (dec % 10)
    
    
    def setDate(self, year, month, day, weekday, hour, minute, second):
        """
        set all values of the RTC
        """
        self.i2c.writeto(self._addr,
                         bytes([self.RTCSECOND, self._decToHex(second % 60), self._decToHex(minute % 60),
                                self._decToHex(hour % 24), self._decToHex(weekday % 8), self._decToHex(day % 32),
                                self._decToHex(month % 13), self._decToHex(year % 100)]))
        
        
    def setYear(self, year):
        """
        set year on RTC
        """
        self._writeReg(self.RTCYEAR, self._decToHex(year % 100))
        
        
    def setMonth(self, month):
        """
        set month on RTC
        """
        self._writeReg(self.RTCMONTH, self._decToHex(month % 13))
        
        
    def setDay(self, day):
        """
        set day on RTC
        """
        self._writeReg(self.RTCDAY, self._decToHex(day % 32))
        
        
    def setWeekday(self, weekday):
        """
        set weekday on RTC
        """
        self._writeReg(self.RTCWEEKDAY, self._decToHex(weekday % 8))
    
    
    def setHour(self, hour):
        """
        set hour on RTC
        """
        self._writeReg(self.RTCHOUR, self._decToHex(hour % 24))
        
        
    def setMinute(self, minute):
        """
        set minute on RTC
        """
        self._writeReg(self.RTCMINUTE, self._decToHex(minute % 60))
        
        
    def setSecond(self, second):
        """
        set second on RTC
        """
        self._writeReg(self.RTCSECOND, self._decToHex(second % 60))
        
        
    def getDate(self):
        """
        read all data from RTC
        """
        return self.getYear(), self.month[self.getMonth()-1], self.getDay(), self.weekday[self.getWeekday()-1], self.getHour(), self.getMinute(), self.getSecond()
    
    
    def getYear(self):
        """
        read year from RTC
        """
        return min(self._hexToDec(self._readReg(self.RTCYEAR)), 99) + 2000
    
    
    def getMonth(self):
        """
        read month from RTC
        """
        return max(min(self._hexToDec(self._readReg(self.RTCMONTH)), 31), 1)
    
    
    def getDay(self):
        """
        read day from RTC
        """
        return max(min(self._hexToDec(self._readReg(self.RTCDAY)), 31), 1)
    
    
    def getWeekday(self):
        """
        read weekday from RTC
        """
        return max(min(self._hexToDec(self._readReg(self.RTCWEEKDAY)), 7), 1)
    
    
    def getHour(self):
        """
        read hour from RTC
        """
        return min(self._hexToDec(self._readReg(self.RTCHOUR)), 23)
    
    
    def getMinute(self):
        """
        read minute from RTC
        """
        return min(self._hexToDec(self._readReg(self.RTCMINUTE)), 59)
    
    
    def getSecond(self):
        """
        read second from RTC
        """
        return min(self._hexToDec(self._readReg(self.RTCSECOND)), 59)
