import utime

class MS5607:
    RESET = 0x1E
    READ = 0x00
    CONV = 0x40
    D1 = 0x00
    D2 = 0x10
    PROM_RD = 0xA0
    ADC_RESOLUTION = {256: 0x00,
                      512: 0x02,
                      1024: 0x04,
                      2048: 0x06,
                      4096: 0x08}
    ADC_DELAY = {0x00: 1,
                  0x02: 3,
                  0x04: 4,
                  0x06: 6,
                  0x08: 10}
    
    
    def __init__(self, i2c, addr = 0x77, res = 4096):
        """
        i2c - i2c port
        addr - adress of MCP23008
        res - resolution of the barometer
        """
        self._addr = addr
        self.i2c = i2c
        self.coeff = []
        self._res = self.ADC_RESOLUTION[res]
    
    
    def begin(self):
        """
        start communication with barometer
        """
        self.reset()
        self.coeff = self._getCoeffs()
        
        
    def reset(self):
        """
        reset barometer
        """
        self.i2c.writeto(self._addr, bytes([self.RESET]))
    
    
    def _readCoeff(self, num):
        """
        read one coefficent
        num - index of coefficent
        """
        self.i2c.writeto(self._addr, bytes([(self.PROM_RD + (num * 2))]))
        result = self.i2c.readfrom(self._addr, 2)
        return (256 * result[0]) + result[1]
    
    
    def _getCoeffs(self):
        """
        read all coefficents from barometer
        """
        cx = 6 * [0]
        for i in range(6):
            utime.sleep(0.01)
            cx[i] = self._readCoeff(i+1)
            if cx[i] == 0: cx[i] = self._readCoeff(i+1)    
        return cx
    
    def _conversion(self, data):
        """
        convert measured values
        """
        self.i2c.writeto(self._addr, bytes([(self.CONV | data | self._res)]))
        utime.sleep_ms(self.ADC_DELAY[self._res])
        self.i2c.writeto(self._addr, bytes([self.READ]))
        converted = self.i2c.readfrom(self._addr, 3)
        return (65536 * converted[0]) + (256 * converted[1]) + converted[2]
    
    
    def get_pressure(self):
        """
        read the measured pressure from barometer 
        """
        d1 = self._conversion(self.D1)
        d2 = self._conversion(self.D2)
        dT = d2 - (self.coeff[4] * 256)
        off = self.coeff[1] * 131072 + (self.coeff[3] * dT) / 64
        sens = self.coeff[0] * 65536 + (self.coeff[2] * dT) / 128
        return round(((d1 * sens / 2097152 - off) / 32768) / 100, 2)
    
    
    def get_temperature(self):
        """
        read the measured temperature from barometer
        """
        d2 = self._conversion(self.D2)
        dT = d2 - (self.coeff[4] * 256)
        return round((2000 + dT * (self.coeff[5] / 8388608)) / 100, 2)
        
        
    def get_altitude(self, reference_pressure = 1013.25):
        """
        calculates altitude from the measured pressure
        reference_pressure - mean sea level pressure,  should be adjusted to local QNH
        """
        return round(44330 * (1 - (self.get_pressure() / reference_pressure) ** (1/5.255)), 2)
        
        