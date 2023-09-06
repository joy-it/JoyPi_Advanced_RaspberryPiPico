import machine
    
class ADC_TLA2518:
    SYSTEM_STATUS = 0x00
    READ_CMD = 0x10
    WRITE_CMD = 0x08
    CHANNEL_SEL = 0x11
    PIN_CFG = 0x05
    SEQUENCE_CFG = 0x10
    
    def __init__(self,spi, cs = 17):
        """
        initialize ADC
        bus - select bus
        device - select device
        """
        self.spi = spi
        self.cs = machine.Pin(cs, machine.Pin.OUT)
    
    def begin():
        """
        """
        self.cs.value(1)
        data = self.read_register(self.SEQUENCE_CFG)
        self.write_register(self.SEQUENCE_CFG, data[0] & 0xFC)
        self.write_register(self.PIN_CFG, 0x00)
        self.write_register(self.SEQUENCE_CFG, 0x00)
        
    def read_value(self, channel):      
        """
        returns raw value from a specific channel
        channel - which channel should be read from
        """ 
        self.write_register(self.CHANNEL_SEL, channel)
        
        self.cs.value(0)
        self.spi.read(2)
        self.cs.value(1)
        
        self.cs.value(0)
        data = self.spi.read(2)
        self.cs.value(1)
        return ((data[0]<<8) | data[1]) >>4
 
    def read_voltage(self, channel, value = None): 
        """
        returns measured voltage from a specific channel
        channel - which should be read from
        value - if channel is already read, raw value can be then used to calculate voltage
        """
        if value is None:  
            return round((self.read_value(channel) / 4096) * 5.0, 2)
        return round((value / 4096) * 5.0, 2)
        
    def read_register(self, reg):
        """
        returns value from a specific register
        reg - register which should be read from
        """
        self.cs.value(0)
        self.spi.write(bytearray([self.READ_CMD, reg, 0x00]))
        data = self.spi.read(1)
        self.cs.value(1)
        return data
        
    def write_register(self, reg, data):
        """
        write value into a specific register
        reg - register in which should be written
        data - value which should be written into the register
        """
        self.cs.value(0)
        self.spi.write(bytearray([self.WRITE_CMD, reg, data]))
        self.cs.value(1)
        
    def read_status(self):
        """
        return status of the ADC
        """
        return self.read_register(self.SYSTEM_STATUS)
        
    
        
                 
                                                                