import utime

# Class to communicate with MCP23008
class MCP23008:
    
    IODIR   = 0x00
    IPOL    = 0x01
    GPINTEN = 0x02
    DEFVAL  = 0x03
    INTCON  = 0x04
    IOCON   = 0x05
    GPPU    = 0x06
    INTF    = 0x07
    INTCAP  = 0x08
    GPIO    = 0x09
    OLAT    = 0x0A
    
    def __init__(self, i2c, addr):
        """
        i2c - i2c port
        addr - adress of MCP23008
        """
        self._addr = addr
        self.i2c = i2c
        
        
    def _write_register(self, reg, data):
        """
        writes data to register
        """
        self.i2c.writeto_mem(self._addr, reg, bytes([data]))
        
        
    def _read_register(self, reg):
        """
        reads data from register
        """
        return self.i2c.readfrom_mem(self._addr, reg, 1)[0]


    def set_pin_direction(self, pin, direction):
        """
        set GPIOs from MCP23008 as input or as output
        """
        current_value = self._read_register(self.IODIR)
        if direction == "OUT":
            self._write_register(self.IODIR, current_value & ~(1 << pin))
        else:
            self._write_register(self.IODIR, current_value | (1 << pin))
    
    
    def set_pin_value(self, pin, value):
        """
        set GPIO from MCP23008 high or low
        """
        current_value = self._read_register(self.GPIO)
        if value == 1:
            self._write_register(self.GPIO, current_value | (1 << pin))
        else:
            self._write_register(self.GPIO, current_value & ~(1 << pin))
    
    
    def set_all_pins_to_same_value(self, value):
        """
        set all GPIOs high or low
        """
        if value == 1:
            self._write_register(self.GPIO, 0xFF)
        else:
            self._write_register(self.GPIO, 0x00)
    
    
    def get_pin_value(self, pin):
        """
        read value from specific GPIO
        """
        return (self._read_register(self.GPIO) >> pin) & 1
    
    
    def get_pin_values(self):
        """
        read values from all GPIOs
        """
        return self._read_register(self.GPIO)
    
    
    def activate_pullUp(self, pin):
        """
        activate PullUp resistor to a certain GPIO of the MCP23008
        """
        current_value = self._read_register(self.GPPU)
        self._write_register(self.GPPU, current_value | (1 << pin))
        
        
    def set_inverted_polarity(self, pin, invert=True):
        """
        set inverted polarity to a specific GPIO of MCP23008
        """
        current_value = self._read_register(self.IPOL)
        if invert:
            self._write_register(self.IPOL, current_value | (1 << pin))
        else:
            self._write_register(self.IPOL, current_value & ~(1 << pin))
            

# Class to controll button matrix
class Buttonmatrix:
    
    # values shown on the button matrix
    dictionary = {(0, 0) : "7",
                  (0, 1) : "4",
                  (0, 2) : "1",
                  (0, 3) : "0",
                  (1, 0) : "8",
                  (1, 1) : "5",
                  (1, 2) : "2",
                  (1, 3) : "#",
                  (2, 0) : "9",
                  (2, 1) : "6",
                  (2, 2) : "3",
                  (2, 3) : "=",
                  (3, 0) : "*",
                  (3, 1) : "/",
                  (3, 2) : "+",
                  (3, 3) : "-"}
    
    def __init__(self, i2c, addr = 0x22):
        """
        i2c - i2c port
        i2c_address - address of the MCP23008 whcih is connected to the buttonmatrix
        """
        self.mcp = MCP23008(i2c, addr)
        self.calculated = ""
        
        
    def begin(self):
        """
        setup MCP23008 to read button matrix
        """
        self.mcp.set_all_pins_to_same_value(0)
        self.mcp._write_register(0x00, 0x0F)
        self.mcp._write_register(0x06, 0x0F)
        
        
    def _checkMatrix(self):
        """
        check which button was pressed
        """
        col_pos, row_pos = -1, -1
        check_column = self.mcp.get_pin_values()

        if check_column == 0x0E:
            col_pos = 0
        elif check_column == 0x0D:
            col_pos = 1
        elif check_column == 0x0B:
            col_pos = 2
        elif check_column == 0x07:
            col_pos = 3
        else:
            return False
        
        check_row_flag = False
        self.mcp.set_all_pins_to_same_value(0)
        
        self.mcp.set_pin_value(4, 1)
        check_row = self.mcp.get_pin_values()

        if check_row == 0x1F:
            row_pos = 0
            check_row_flag = True         
        
        if check_row_flag == False:
            self.mcp.set_all_pins_to_same_value(0)
            self.mcp.set_pin_value(5, 1)
            check_row = self.mcp.get_pin_values()
            if check_row == 0x2F:
                row_pos = 1
                check_row_flag = True
            
        if check_row_flag == False:
            self.mcp.set_all_pins_to_same_value(0)
            self.mcp.set_pin_value(6, 1)
            check_row = self.mcp.get_pin_values()
            if check_row == 0x4F:
                row_pos = 2
                check_row_flag = True
        
        if check_row_flag == False:
            self.mcp.set_all_pins_to_same_value(0)
            self.mcp.set_pin_value(7, 1)
            check_row = self.mcp.get_pin_values()
            if check_row == 0x8F:
                row_pos = 3
                check_row_flag = True       
            
        self.mcp.set_all_pins_to_same_value(0)
        utime.sleep(.1)
        return col_pos, row_pos

        
    def getKey(self):
        """
        returns the name of the button which was pressed
        """
        try:
            return self.dictionary[self._checkMatrix()]
        except KeyError:
            return None


    def clearMemory(self):
        """
        clears class variable calculated
        """
        self.calculated = ""
        
        
    def calculate(self):
        """
        method to use button matrix as calculator
        """
        value = self.getKey()
        if value is None:
            return self.calculated
        if value == "=":
            try:
                self.calculated = str(eval(self.calculated))
                return self.calculated
            # catch if number should be divided by zero
            except ZeroDivisionError :
                self.clearMemory()
                raise ValueError("You can not divide by zero!")
            # catch if string is not convertable to a number
            except SyntaxError:
                self.clearMemory()
                raise ValueError("Term can not be calculated!")
        elif value == "#":
            self.clearMemory()
        else:
            self.calculated += value
            return self.calculated