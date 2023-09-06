import machine

class ICG1020S:

    scaleFactor = 0
    scale_gyroscope = 700
    scale_range = 46.5
    offset = 0
    
    def __init__(self, spi, cs = 27):
        """
        initialize gyroscope
        spi - get established spi communication
        cs - set chip select
        """
        self.spi = spi
        self.cs = machine.Pin(cs, machine.Pin.OUT)
        
        
    def begin(self):
        self.cs.high()
        tmp = self.read_register(27) & 0x26
        self.write_register(27, 0x18 | tmp)
        
        
    def read_register(self, reg):
        """
        read value from register
        """
        self.cs.value(0)
        self.spi.write(bytearray([(reg | 0x80)]))
        data = self.spi.read(1)
        self.cs.value(1)        
        return data[0]

        
    def write_register(self, reg, data):
        """
        write value to register
        """
        self.cs.value(0)
        self.spi.write(bytearray([(reg & 0x7F), data]))
        self.cs.value(1)
       
        
    def getTemperature(self):
        """
        returns read temnperature
        """
        temp = (self.read_register(0x41) << 8) | self.read_register(0x42)
        return (temp / 100)

    
    def getXValue(self):
        """
        returns x value
        """
        x = (self.read_register(0x43) << 8) | self.read_register(0x44)
        if (x / self.scale_gyroscope > self.scale_range):
            return x / self.scale_gyroscope - (2 * self.scale_range)
        else:
            return x / self.scale_gyroscope

    
    def getYValue(self):
        """
        returns y value
        """
        y = (self.read_register(0x45) << 8) | self.read_register(0x46)
        if (y / self.scale_gyroscope > self.scale_range):
            return y / self.scale_gyroscope - (2 * self.scale_range)
        else:
            return y / self.scale_gyroscope

    
    def getTilt(self):
        """
        returns tilt directions
        """
        y = self.getYValue()
        x = self.getXValue()
        if (y > 2):
            return 'right'
        elif (y < -2):
            return 'left'
        elif (x > 2):
            return 'backwards'
        elif (x < -2):
            return 'forwards'
        else:
            return 'No movement'

        
    def who_am_i(self):
        """
        returns device ID
        """
        return (self.read_register(0x75))
                
                
    def scale_Factor(self, scale):
        """
        set scale factor of gyroscope
        """
        self.scaleFactor = scale
        self.write_register(0x19, 0)
        self.write_register(0x1B, scale +1)
        if (scale == 0):
            self.scale_gyroscope = 700
            self.scale_range = 46.5
        
        elif (scale == 8): 
            self.scale_gyroscope = 350
            self.scale_range = 93
        
        elif (scale == 16): 
            self.scale_gyroscope = 175
            self.scale_range = 187
        
        elif (scale == 24): 
            self.scale_gyroscope = 87.5
            self.scale_range = 374        