import utime

# ++++++++++++++++++++++++++ RGB_Matrix object ++++++++++++++++++++++++++
class RGB_Matrix:
    """
    New version using the I2C-based PixelStrip instead of rpi_ws281x.
    """

    def __init__(self, i2c, i2c_adress = 0x66, count = 64, brightness = 80, 
                 right_border = [7,15,23,31,39,47,55,63], left_border = [0,8,16,24,32,40,48,56]):
        """
        initiliaze LED matrix
        
        :param count: amount of LEDs in matrix
        :param brightness: brightness level of all pixels
        :param right_border: reference values for all pixel on the right side
        :param left_border: reference values for all pixel on the left side
        """
        # LED configuration
        self.LED_COUNT = count
        self.LED_BRIGHTNESS = brightness

        # For reference if needed
        self.RIGHT_BORDER = right_border
        self.LEFT_BORDER  = left_border

        # Create the I2C-based PixelStrip instance
        self.strip = PixelStrip(num=self.LED_COUNT, i2c=i2c, brightness=self.LED_BRIGHTNESS, i2c_adress=i2c_adress)
        self.strip.begin()

    def clean(self):
        """
        Turn off all pixels
        """
        self.RGB_off()

    def setPixel(self, position, colour):
        """
        set pixel at position to colour
        
        :param position: Pixel position index
        :param colour: RGBW value 32 bit integer or tuple
        """
        self.strip.setPixelColor(position, colour)

    def RGB_on(self, colour):
        """
        set all pixel of matrix to colour
        
        :param colour: RGBW value 32 bit integer or tuple
        """
        for i in range(self.strip.getNumPixels()):
            self.strip.setPixelColor(i, colour)
        self.strip.show()

    def RGB_off(self):
        """
        turn all LEDs in matrix off
        """
        for i in range(self.strip.getNumPixels()):
            self.strip.setPixelColor(i, RGBW(0, 0, 0, 0))
        self.strip.show()

    def wheel(self, pos):
        """
        generate rainbow colours over positions 0-255

        :param pos: selected pixel
        """
        if pos < 85:
            return RGBW(pos * 3, 255 - pos * 3, 0, 0).unpackHEX()
        elif pos < 170:
            pos -= 85
            return RGBW(255 - pos * 3, 0, pos * 3, 0).unpackHEX()
        else:
            pos -= 170
            return RGBW(0, pos * 3, 255 - pos * 3, 0).unpackHEX()

    def rainbow(self, wait_ms=20, iterations=1):
        """
        Rainbow effect on all LEDs

        :param wait_ms: time in between colour change per pixel
        :param iterations: iterations of animation
        """
        for j in range(256 * iterations):
            for i in range(self.strip.getNumPixels()):
                self.strip.setPixelColor(i, self.wheel((i + j) & 255))
            self.strip.show()
            utime.sleep_ms(wait_ms)

    def colourWipe(self, color, wait_ms=50):
        """
        Move colours pixel by pixel over the LEDs with a given colour

        :param color: RGB value to set pixels to
        :param wait_ms: time between each pixel
        """
        for i in range(self.strip.getNumPixels()):
            self.strip.setPixelColor(i, color)
            self.strip.show()
            utime.sleep_ms(wait_ms)

    def theaterChase(self, color, wait_ms=50, iterations=10):
        """
        Chaser animation with a given colour

        :param color: RGB value (RGBW or tuple) to set pixels to
        :param wait_ms: time in between colour change per pixel
        :param iterations: iterations of animation
        """
        for j in range(iterations):
            for q in range(3):
                for i in range(0, self.strip.getNumPixels(), 3):
                    self.strip.setPixelColor(i + q, color)
                self.strip.show()
                utime.sleep_ms(wait_ms)
                for i in range(0, self.strip.getNumPixels(), 3):
                    self.strip.setPixelColor(i + q, 0)

    def demo1(self):
        """
        Simple demo programm
        """
        self.theaterChase(RGBW(127, 127, 127, 0))  # White chaser
        self.theaterChase(RGBW(127, 0, 0, 0))  # Red chaser
        self.theaterChase(RGBW(0, 0, 127, 0)) # Blue chaser
        self.rainbow()
        self.clean()

    def show(self):
        """
        show changes on LED matrix
        """
        self.strip.show()

    def demo2(self):
        """
        More complex demo programm in a continuous loop
        """
        heart = [1,6,8,9,10,13,14,15,16,17,18,19,20,21,22,23,
                         24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,
                         41,42,43,44,45,46,50,51,52,53,59,60]
        try:
            for i in range(3):
                self.demo1()
            while True:
                for i in heart:
                    self.strip.setPixelColor(i, RGBW(255, 0, 0, 0))
                self.strip.show()
        except KeyboardInterrupt:
            self.clean()
    
    def setBrightness(self, brightness):
        """
        Set brightness of all pixels

        :param brightness: brightness level (0-255)
        """
        self.strip.setBrightness(brightness)
        self.strip.show()
    
    def getPixelNum(self):
        """
        Get number of pixels in matrix
        """
        return self.strip.getNumPixels()

# ++++++++++++++++++++++++++ RGBW object ++++++++++++++++++++++++++  
class RGBW:
    """
    Represents a 32-bit RGBW color value.

    This class allows combining separate red, green, blue, and optional white
    components into a single 32-bit integer while still providing convenient
    access to each color channel via properties.

    Format (32-bit):
        [ W (8 bit) | R (8 bit) | G (8 bit) | B (8 bit) ]
    """

    def __init__(self, r, g=None, b=None, w=None):
        """
        Create a new RGBW color value. The object can be initialized in two ways:
        1) With a single integer: RGBW(0xWWRRGGBB)
        2) With individual color components: RGBW(r, g, b, w=0)

        :param r: Red value (0–255) or packed 32-bit integer
        :param g: Green value (0–255)
        :param b: Blue value (0–255)
        :param w: White value (0–255), optional (default = 0)
        """
        if (g, b, w) == (None, None, None):
            self._value = r
        else:
            if w is None:
                w = 0
            self._value = (w << 24) | (r << 16) | (g << 8) | b

    def unpackRGBW(self):
        return self.getRed(), self.getGreen(), self.getBlue(), self.getWhite()
    
    def unpackHEX(self):
        return self._value
    
    @property
    def getRed(self):
        """
        get red value
        """
        return (self._value >> 16) & 0xff

    @property
    def getGreen(self):
        """
        get green value
        """
        return (self._value >> 8) & 0xff

    @property
    def getBlue(self):
        """
        get blue value
        """
        return self._value & 0xff

    @property
    def getWhite(self):
        """
        get white value
        """
        return (self._value >> 24) & 0xff

# ++++++++++++++++++++++++++ enum for led matrix functions ++++++++++++++++++++++++++   
class FunctionEnum:
    """
    Command identifiers used for controlling the LED matrix
    via I2C communication.

    Each value represents a specific function that can be executed by the
    LED controller firmware, such as pixel manipulation, brightness control,
    gamma correction, color conversion, or data transmission.
    """
    SHOW                = 0
    SETPIXELCOLOR       = 1
    FILL                = 2
    SETBRIGHTNESS       = 3
    GAMMA8              = 4
    GAMMA32             = 5
    NUMPIXEL            = 6
    COLORHSV            = 7
    CLEAR               = 8
    SENDDATA2SHOW       = 9
    SENDALLPIXRGB0      = 10
    SENDALLPIXRGB1      = 11
    SENDALLPIXRGB2      = 12
    SENDALLPIXRGB3      = 13
    SENDALLPIXRGB4      = 14
    SENDALLPIXRGB5      = 15

# ++++++++++++++++++++++++++ PixelStrip object ++++++++++++++++++++++++++
class PixelStrip:
    """
    Controls a strip of LEDs (WS281x / SK6812) via I2C.
    """

    def __init__(self, num, i2c, brightness=255, i2c_adress = 0x66):
        """
        initilize LED controll class
        
        :param num: amount of pixel to controll
        :param brightness: brightness of all pixels
        """
        self.num = num
        self.address = i2c_adress
        self.i2c = i2c
        self.transfer_data = LEDTransferData()
        self.transfer_data.setBright(brightness)

    def begin(self):
        """
        Set the initial brightness on the hardware side via I2C
        """
        self.transfer_data.setFunc(FunctionEnum.SETBRIGHTNESS)
        self.send(0x00)

    def send(self, cmd):
        """
        Send a block of data to the device using I2C

        :param cmd: block of data to send
        """
        data = bytes([
            cmd & 0xFF,
            0x0C,
            self.transfer_data.func & 0xFF,
            self.transfer_data.pos & 0xFF,
            self.transfer_data.r & 0xFF,
            self.transfer_data.g & 0xFF,
            self.transfer_data.b & 0xFF,
            self.transfer_data.w & 0xFF,
            self.transfer_data.c & 0xFF,
            self.transfer_data.bright & 0xFF,
            self.transfer_data.first & 0xFF,
            self.transfer_data.count & 0xFF,
            self.transfer_data.data & 0xFF,
            self.transfer_data.data1 & 0xFF,
        ])
        self.i2c.writeto(self.address, data)
        utime.sleep_ms(3)  # Hardware timing delay
        self.transfer_data.clean()

    def _write(self, cmd, data):
        """
        Send a command byte followed by a data block
        """
        buffer = bytes([cmd & 0xFF, len(data) & 0xFF] + [value & 0xFF for value in data])
        self.i2c.writeto(buffer)
        utime.sleep_ms(3)

    def _read(self):
        """
        Read one byte from the I2C device
        """
        return int.from_bytes(self.i2c.readfrom_mem(self.address, reg, 1), 'little')
    
    def __len__(self):
        """
        Return the total number of pixels
        """
        return self.num

    def clear(self):
        """
        Clear the entire LED strip (turn off all pixels)
        """
        self.transfer_data.setFunc(FunctionEnum.CLEAR)
        self.send(0x00)

    def show(self):
        """
        Show updated pixel data on the LED strip
        """
        self.transfer_data.setFunc(FunctionEnum.SHOW)
        self.send(0x00)

    def getWRGB(self, color):
        """
        Extract W, R, G, B values from a single color int

        :param color: single color int
        """
        if isinstance(color, RGBW):
            color = color.unpackHEX()
        elif not isinstance(color, int):
            return 0 & 0xffffffff
        return (
            (color >> 24) & 0xff, 
            (color >> 16) & 0xff, 
            (color >> 8)  & 0xff, 
            color & 0xff
        )

    def setPixelColor(self, n, color):
        """
        Set a single pixel (at index n) to the specified 32-bit color

        :param n: Pixel position index
        :param color: 32-bit color or tupel of (r,g,b) or (r,g,b,w)
        """
        self.transfer_data.setPos(n)
        if isinstance(color, tuple):
            if len(color) == 3:
                r, g, b = color
                w = 0
            elif len(color) == 4:
                r, g, b, w = color
        else:
            w, r, g, b = self.getWRGB(color)
        self.setPixelColorRGB(n, r, g, b, w)

    def setPixelColorRGB(self, n, red, green, blue, white=0):
        """
        set Pixel colour at specific index

        :param n: Pixel position index
        :param red: colour value of red
        :param green: colour value of green
        :param blue: colour value of blue
        :param white: colour value of white - default 0
        """
        self.transfer_data.setPos(n)
        self.transfer_data.setR(red)
        self.transfer_data.setG(green)
        self.transfer_data.setB(blue)
        self.transfer_data.setW(white)
        self.transfer_data.setC(0)
        self.transfer_data.setFunc(FunctionEnum.SETPIXELCOLOR)
        self.send(0x00)

    def sendPos2Show(self, pos, r=0, g=0, b=0):
        """
        Sends color data to selected pixel positions and immediatly dislpays update
        
        :param pos: Pixel position index
        :param r: colour value of red
        :param g: colour value of green
        :param b: colour value of blue
        """
        self.transfer_data.setR(r)
        self.transfer_data.setG(g)
        self.transfer_data.setB(b)
        for i in pos:
            if 0 <= i <= 7:
                self.transfer_data.pos |= 1 << i
            elif 8 <= i <= 15:
                self.transfer_data.w |= 1 << (i - 8)
            elif 16 <= i <= 23:
                self.transfer_data.c |= 1 << (i - 16)
            elif 24 <= i <= 31:
                self.transfer_data.bright |= 1 << (i - 24)
            elif 32 <= i <= 39:
                self.transfer_data.first |= 1 << (i - 32)
            elif 40 <= i <= 47:
                self.transfer_data.count |= 1 << (i - 40)
            elif 48 <= i <= 55:
                self.transfer_data.data |= 1 << (i - 48)
            elif 56 <= i <= 63:
                self.transfer_data.data1 |= 1 << (i - 56)
        self.transfer_data.setFunc(FunctionEnum.SENDDATA2SHOW)
        self.send(0x00)

    def sendColor2Show(self, pos, color=0):
        """
        write RGB value onto pixel at specific index
        
        :param pos: Pixel position index
        :param color: RGB value (RGBW or tuple) to write onto pixel
        """
        if isinstance(color, tuple):
            if len(color) == 3:
                r, g, b = color
                w = 0
            elif len(color) == 4:
                r, g, b, w = color
        else:
            w, r, g, b = self.getWRGB(color)
        self.transfer_data.setR(r)
        self.transfer_data.setG(g)
        self.transfer_data.setB(b)
        self.sendPos2Show(pos, r, g, b)

    def sendAllPixRGB(self, rgb):
        """
        Send large RGB data (6 chunks of 32 bytes each) to fill multiple pixels

        :param self: Description
        :param rgb: RGB value to write onto pixels
        """
        for i in range(6):
            start = 32 * i
            end = start + 32
            self._write( FunctionEnum.SENDALLPIXRGB0 + i, rgb[start:end])

    def fill(self, r=0, g=0, b=0, w=0, first=0, end=64):
        """
        write same RGB value from pixel with one index to another 

        :param r: colour value of red
        :param g: colour value of green
        :param b: colour value of blue
        :param w: colour value of white
        :param first: index of pixel to begin writing color on
        :param end: index of pixel to end writing colour on
        """
        self.transfer_data.setR(r)
        self.transfer_data.setG(g)
        self.transfer_data.setB(b)
        self.transfer_data.setW(w)
        self.transfer_data.setFirst(first)
        self.transfer_data.setCount(end - first)
        self.transfer_data.setFunc(FunctionEnum.FILL)
        self.send(0x00)

    def fillColor(self, color, first=0, end=63):
        """
        write same RGB value from pixel with one index to another 

        :param color: RGBW value to write onto pixels
        :param first: index of pixel to begin writing color on
        :param end: index of pixel to end writing colour on
        """
        if isinstance(color, tuple):
            if len(color) == 3:
                r, g, b = color
                w = 0
            elif len(color) == 4:
                r, g, b, w = color
        else:
            w, r, g, b = self.getWRGB(color)
        self.fill(r, g, b, w, first, end)

    def setBrightness(self, brightness):
        """
        Set global brightness for all pixels
        
        :param brightness: set brightness to all pixels
        """
        self.transfer_data.setBright(brightness)
        self.transfer_data.setFunc(FunctionEnum.SETBRIGHTNESS)
        self.send(0x00)

    def getNumPixels(self):
        """
        Return the number of pixels in this strip
        """
        return self.num

    def getGamma8(self, x):
        """
        Applies 8-bit gamma correction to the given input value.

        :param x: 8-bit input value (0-255)
        """
        self.transfer_data.setFunc(FunctionEnum.GAMMA8)
        self.transfer_data.setData(x)
        self.send(0x01)
        return self._read()

    def getGamma32(self, x):
        """
        Applies 32-bit gamma correction to the given input value.

        :param x: 32-bit input value
        """
        self.transfer_data.setFunc(FunctionEnum.GAMMA32)
        self.transfer_data.setData(x)
        self.send(0x01)
        return self._read()

    def getColorHSV(self, x):
        """
        Converts an HSV color value into the device-specific RGB format.

        :param x: HSV input value (device-dependent encoding)
        """
        self.transfer_data.setFunc(FunctionEnum.COLORHSV)
        self.transfer_data.setData(x)
        self.send(0x01)
        return self._read()

# ++++++++++++++++++++++++++ LEDTransferData object ++++++++++++++++++++++++++
class LEDTransferData:
    """
    Data container class used to prepare and store parameters for I2C
    communication with the LED controller.

    This class encapsulates all fields required to build a command packet,
    including function identifiers, pixel position, color values, brightness,
    and range parameters for bulk operations.
    """
    def __init__(self, func=0, pos=0, r=0, g=0, b=0, w=0, c=0, bright=5, first=0, count=0):
        """
        Initialize the data structure for an LED control command
        
        :param func: Function ID (see FunctionEnum)
        :param pos: Pixel position index
        :param r: Red color component (0–255)
        :param g: Green color component (0–255)
        :param b: Blue color component (0–255)
        :param w: White color component (for RGBW LEDs)
        :param c: Additional color or control parameter (device-dependent)
        :param bright: Global brightness level
        :param first: First pixel index for range operations
        :param count: Number of pixels affected in range operations
        """
        self.func   = func
        self.pos    = pos
        self.r      = r
        self.g      = g
        self.b      = b
        self.w      = w
        self.c      = c
        self.bright = bright
        self.first  = first
        self.count  = count
        self.data   = 0
        self.data1  = 0

    def setFunc(self, func=0):
        """
        set Function ID

        :param func: Function ID - default = 0 - SHOW
        """
        self.func = func
    
    def setPos(self, pos=0):
        """
        set Pixel position index
        
        :param pos: Pixel position index - default = 0
        """
        self.pos = pos
    
    def setR(self, r=0):
        """
        set Red color component

        :param r: Red color component - default = 0
        """
        self.r = r
    
    def setG(self, g=0):
        """
        set Green color component 

        :param g: Green color component - default = 0
        """
        self.g = g
    
    def setB(self, b=0):
        """
        set Blue color component
        
        :param b: Blue color component - default = 0
        """
        self.b = b
    
    def setW(self, w=0):
        """
        set White color component
        
        :param w: White color component - default = 0
        """
        self.w = w
    
    def setC(self, c=0):
        """
        set Additional color or control parameter
        
        :param c: Additional color or control parameter - default = 0
        """
        self.c = c
    
    def setFirst(self, first=0):
        """
        set First pixel index for range operations
        
        :param first: First pixel index for range operations - default = 0
        """
        self.first = first
    
    def setCount(self, count=0):
        """
        set Number of pixels affected in range operations
        
        :param count: Number of pixels affected in range operations - default = 0
        """
        self.count = count
    
    def setBright(self, bright=0):
        """
        set Global brightness level

        :param bright: Global brightness level - default = 0
        """
        self.bright = bright
    
    def setData(self, data=0):
        """
        Sets the primary data value for the I²C command packet.

        This value is typically used to store a processed or combined
        parameter (e.g., color value, gamma result, or control data)
        before transmission.
        
        :param data: Integer value to be assigned to the primary data field - default = 0
        """
        self.data = data
    
    def setData1(self, data=0):
        """
        Sets the secondary data value for the I²C command packet.

        This field is commonly used for additional parameters such as
        high/low bytes, extended data, or supplementary command values.
        
        :param data: Integer value to be assigned to the secondary data field - default = 0
        """
        self.data1 = data

    def clean(self):
        """
        Reset all internal fields to zero after transmission
        """
        self.func   = 0
        self.pos    = 0
        self.r      = 0
        self.g      = 0
        self.b      = 0
        self.w      = 0
        self.c      = 0
        self.bright = 0
        self.first  = 0
        self.count  = 0
        self.data   = 0
        self.data1  = 0
