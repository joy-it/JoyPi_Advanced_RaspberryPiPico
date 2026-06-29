import utime
import machine
from machine import Pin

class ST7735:
    
    NOP = 0x00
    SWRESET = 0x01
    RDDID = 0x04
    RDDST = 0x09
    
    SLPIN = 0x10
    SLPOUT = 0x11
    PTLON = 0x12
    NORON = 0x13
    
    INVOFF = 0x20
    INVON = 0x21
    DISPOFF = 0x28
    DISPON = 0x29
    CASET = 0x2A
    RASET = 0x2B
    RAMWR = 0x2C
    RAMRD = 0x2E
    
    PTLAR = 0x30
    COLMOD = 0x3A
    MADCTL = 0x36
    
    FRMCTR1 = 0xB1
    FRMCTR2 = 0xB2
    FRMCTR3 = 0xB3
    INVCTR = 0xB4
    DISSET5 = 0xB6
    
    PWCTR1 = 0xC0
    PWCTR2 = 0xC1
    PWCTR3 = 0xC2
    PWCTR4 = 0xC3
    PWCTR5 = 0xC4
    VMCTR1 = 0xC5
    
    RDID1 = 0xDA
    RDID2 = 0xDB
    RDID3 = 0xDC
    RDID4 = 0xDD
    
    PWCTR6 = 0xFC
    
    GMCTRP1 = 0xE0
    GMCTRN1 = 0xE1
    
    fontOne = [0x0022D422, 0x0022D422, 0x0022D422, 0x0022D422, 0x0022D422, 0x0022D422,
       0x0022D422, 0x0022D422, 0x0022D422, 0x0022D422, 0x0022D422, 0x0022D422, 0x0022D422, 0x0022D422,
       0x0022D422, 0x0022D422, 0x0022D422, 0x0022D422, 0x0022D422, 0x0022D422]
    fontTwo = [0x0022D422, 0x0022D422, 0x0022D422, 0x0022D422, 0x0022D422, 0x0022D422,
       0x0022D422, 0x0022D422, 0x0022D422, 0x0022D422, 0x0022D422, 0x0022D422, 0x00000000, 0x000002E0,
       0x00018060, 0x00AFABEA, 0x00AED6EA, 0x01991133, 0x010556AA, 0x00000060]
    fontThree = [0x000045C0, 0x00003A20, 0x00051140, 0x00023880, 0x00002200, 0x00021080,
       0x00000100, 0x00111110, 0x0007462E, 0x00087E40, 0x000956B9, 0x0005D629, 0x008FA54C, 0x009AD6B7,
       0x008ADA88, 0x00119531, 0x00AAD6AA, 0x0022B6A2, 0x00000140, 0x00002A00]
    fontFour = [0x0008A880, 0x00052940, 0x00022A20, 0x0022D422, 0x00E4D62E, 0x000F14BE,
       0x000556BF, 0x0008C62E, 0x0007463F, 0x0008D6BF, 0x000094BF, 0x00CAC62E, 0x000F909F, 0x000047F1,
       0x0017C629, 0x0008A89F, 0x0008421F, 0x01F1105F, 0x01F4105F, 0x0007462E]
    fontFive = [0x000114BF, 0x000B6526, 0x010514BF, 0x0004D6B2, 0x0010FC21, 0x0007C20F,
       0x00744107, 0x01F4111F, 0x000D909B, 0x00117041, 0x0008CEB9, 0x0008C7E0, 0x01041041, 0x000FC620,
       0x00010440, 0x01084210, 0x00000820, 0x010F4A4C, 0x0004529F, 0x00094A4C]
    fontSix = [0x000FD288, 0x000956AE, 0x000097C4, 0x0007D6A2, 0x000C109F, 0x000003A0,
       0x0006C200, 0x0008289F, 0x000841E0, 0x01E1105E, 0x000E085E, 0x00064A4C, 0x0002295E, 0x000F2944,
       0x0001085C, 0x00012A90, 0x010A51E0, 0x010F420E, 0x00644106, 0x01E8221E]
    fontSeven = [0x00093192, 0x00222292, 0x00095B52, 0x0008FC80, 0x000003E0, 0x000013F1,
       0x00841080, 0x0022D422]
    
    
    def __init__(self, spi, dc = 26, res = 27, cs = 10, x_offset = 2, y_offset = 1, rgbMode = "bgr"):
        """
        initialize TFT display
        spi - established SPI communication
        dc - DC pin
        res - RESET pin
        CS - chip select
        x_offset - offset of x axis
        y_offset - offset of y axis
        rgbMode - set RGB Mode
        """
        self.spi = spi
        self._dc = machine.Pin(dc, machine.Pin.OUT)
        self._res = machine.Pin(res, machine.Pin.OUT)
        self._cs = machine.Pin(cs, machine.Pin.OUT)
        
        self.width = 128 + x_offset
        self.height = 160 + y_offset
        self.offset = [x_offset, y_offset]
        self.colourMode = rgbMode

        
    def reset(self):
        """
        reset display
        """
        self._res.low()
        utime.sleep_ms(50)
        self._res.high()
        utime.sleep_ms(50)
        
        
    def send(self, command, data):
        """
        method to send commands and data
        """
        self._dc.low()
        self._cs.low()
        self.spi.write(bytearray([command]))
        self._dc.high()
        if isinstance(data, (bytes, bytearray, memoryview)):
            self.spi.write(data)
        else:
            self.spi.write(bytes(data))
        self._cs.high()
        
        
    def setWindow(self, x0, y0, x1, y1):
        """
        sets Window to draw in
        """
        x0, y0 = x0 + self.offset[0], y0 + self.offset[1]
        x1, y1 = x1 + self.offset[0], y1 + self.offset[1]
        self.send(self.CASET, [(x0 >> 8) & 0xFF, x0 & 0xFF, (x1 >> 8) & 0xFF, x1 & 0xFF])
        self.send(self.RASET, [(y0 >> 8) & 0xFF, y0, (y1 >> 8) & 0xFF, y1 & 0xFF])
        
        
    def begin(self):
        """
        setup routine of TFT display
        """
        self.reset()
        #Software reset
        self.send(self.SWRESET, [1])
        #Exit Sleep mode
        self.send(self.SLPOUT, [1])
        #Frame rate control - normal mode
        self.send(self.FRMCTR1, [0x01, 0x2C, 0x2D])
        #Frame rate control - idle mode
        self.send(self.FRMCTR2, [0x01, 0x2C, 0x2D, 0x01, 0x2C, 0x2D])
        # Display inversion control
        self.send(self.INVCTR, [0x07])
        # Display power control
        self.send(self.PWCTR1, [0xA2, 0x02, 0x84])
        self.send(self.PWCTR2, [0x8A, 0x2A])
        self.send(self.PWCTR3, [0x0A, 0x00])
        self.send(self.PWCTR4, [0x8A, 0x2A])
        self.send(self.PWCTR5, [0x8A, 0xEE])
        self.send(self.VMCTR1, [0x0E])
        # Disable inversion
        self.send(self.INVOFF, [])
        # Memory access control
        self.send(self.MADCTL, [0xC8])
        # Set 16-bit color mode
        self.send(self.COLMOD, [0x05])
        # Column address set
        self.send(self.CASET, [0x00, 0x00, 0x00, 0x7F])
        # Row address set
        self.send(self.RASET, [0x00, 0x00, 0x00, 0x9F])
        # Set Gamma
        self.send(self.GMCTRP1, [0x02, 0x1C, 0x07, 0x12, 0x37, 0x32, 0x29, 0x2D, 0x29, 0x25, 0x2B, 0x39, 0x00, 0x01, 0x03, 0x10])
        self.send(self.GMCTRN1, [0x03, 0x1D, 0x07, 0x06, 0x2E, 0x2C, 0x29, 0x2D, 0x2E, 0x2E, 0x37, 0x3F, 0x00, 0x00, 0x02, 0x10])
        # Set normal mode
        self.send(self.NORON, [])
        # Turn display on
        self.turnOn()


    def enterDataMode(self):
        """
        prepare display to get data
        """
        self._dc.low()
        self._cs.low()
        self.spi.write(bytearray([self.RAMWR]))
        self._dc.high()
        
        
    def exitDataMode(self):
        """
        end data transfer
        """
        self._cs.high()
        self._dc.low()
        
        
    def convertColour(self, colour):
        """
        convert tuple to hex
        """
        try:
            if self.colourMode == "bgr":
                b, g, r = colour
            else:
                r, g, b = colour
            return ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
        except:
            return 0x0000
            
        
    def fillRectangle(self, x, y, width, height, colour):
        """
        draw a filled rectangle
        x - left upper corner x-coordinate
        y - left upper corner y-coordinate
        width - width of rectangle
        height - height of rectangle
        colour - rgb tuple
        """
        conv_col = self.convertColour(colour)
        high_colour = (conv_col >> 8) & 0xFF
        low_colour = conv_col & 0xFF
        row_buffer = bytes((high_colour, low_colour)) * width
        rows_per_block = max(1, min(height, 1024 // len(row_buffer)))
        block_buffer = row_buffer * rows_per_block
        complete_blocks = height // rows_per_block
        remaining_rows = height % rows_per_block
        self.setWindow(x, y, x + width - 1, y + height - 1)
        self.enterDataMode()
        for _ in range(complete_blocks):
            self.spi.write(block_buffer)
        if remaining_rows:
            self.spi.write(row_buffer * remaining_rows)
        self.exitDataMode()
    
    def drawRectangle(self, x, y, width, height, colour):
        """
        draw outline of a rectangle
        x - left upper corner x-coordinate
        y - left upper corner y-coordinate
        width - width of rectangle
        height - height of rectangle
        colour - rgb tuple
        """
        if width <= 0 or height <= 0:
            return
        # bottom edge
        self.drawHorizontalLine(x, y, width -1, colour)
        # top edge
        if height > 1:
            self.drawHorizontalLine(x, y + height -1, width -1, colour)
        # left and right edges
        if height > 2:
            self.drawVerticalLine(x, y, height, colour)
            if width > 1:
                self.drawVerticalLine(x + width -1 , y, height, colour)
                
        
        
    def fillTriangle(self, x0, y0, x1, y1, x2, y2, colour):
        """
        draw a filled triangle
        x0 - first corner x-coordinate
        y0 - first corner y-coordinate
        x1 - second corner x-coordinate
        y1 - second corner y-coordinate
        x2 - third corner x-coordinate
        y2 - third corner y-coordinate
        colour - rgb tuple
        """
        conv_col = self.convertColour(colour)
        hColour = (conv_col >> 8) % 256
        lColour = conv_col % 256
        # sort point by y-coordinate y0 <= y1 <= y2
        if y0 > y1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        if y1 > y2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
        if y0 > y1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        # all point on one line
        if y0 == y1 and y1 == y2:
            line_start = min(x0, x1, x2)
            line_end = max(x0, x1, x2)
            self.drawHorizontalLine(line_start, y0, line_end, colour)
            return
        dx01 = x1 - x0
        dy01 = y1 - y0
        dx02 = x2 - x0
        dy02 = y2 - y0
        dx12 = x2 - x1
        dy12 = y2 - y1
        # check if y1 is part of upper or lower part of triangle
        if y1 == y2:
            last_y = y1
        else:
            last_y = y1 - 1
        step_a = 0
        step_b = 0
        # upper part of triangle
        for y in range(y0, last_y + 1):
            if dy01 != 0:
                x_start = x0 + step_a // dy01
            else:
                x_start = x0
            x_end = x0 + step_b // dy02
            step_a += dx01
            step_b += dx02
            if x_start > x_end:
                x_start, x_end = x_end, x_start
            self.drawLine(x_start, y, x_end, y, colour)
        # lower part of triangle
        start_y = last_y + 1
        step_a = dx12 * (start_y - y1)
        step_b = dx02 * (start_y - y0)
        for y in range(start_y, y2 + 1):
            if dy12 != 0:
                x_start = x1 + step_a // dy12
            else:
                x_start = x1
            x_end = x0 + step_b // dy02
            step_a += dx12
            step_b += dx02
            if x_start > x_end:
                x_start, x_end = x_end, x_start
            self.drawLine(x_start, y, x_end, y, colour)
    
    def fill(self, colour):
        """
        fill display in one colour
        """
        self.fillRectangle(0, 0, self.width, self.height, colour)
        
        
    def clear(self):
        """
        fill display black
        """
        self.fill((0, 0, 0))
    
    
    def drawPixel(self, x, y, colour):
        """
        draw pixel on display
        x - x-coordinate
        y - y-coordinate
        colour - rgb tuple
        """
        self.setWindow(x, y, x, y)
        conv_col = self.convertColour(colour)
        self.send(self.RAMWR, [(conv_col >> 8) & 0xFF, conv_col & 0xFF])


    def fillCircle(self, x, y, radius, colour):
        """
        draw filled circle on display
        x - x-coordinate of center
        y - y-coordinate of center
        radius - radius of circle
        colour - rgb tuple
        """
        if radius < 0:
            return
        conv_col = self.convertColour(colour)
        max_width = radius * 2 + 1
        line_buffer = bytes(((conv_col >> 8) & 0xFF, conv_col & 0xFF)) * max_width
        line_view = memoryview(line_buffer)
        # Helper method to draw one clipped horizontal span
        def draw_span(x, y, width):
            if width <= 0:
                return
            # biggest line is outside of display
            if y < 0 or y >= self.height:
                return
            # cut of the left side
            if x < 0:
                width += x
                x = 0
            # cut of right side
            if x + width > self.width:
                width = self.width - x
            if width <= 0:
                return
            self.setWindow(x, y, x + width - 1, y)
            self.enterDataMode()
            self.spi.write(line_view[:width * 2])
            self.exitDataMode()
        
        radius_squared = radius * radius
        x_radius = radius
        # calculate on one side and draw simultainisly
        for y_offset in range(radius + 1):
            y_squared = y_offset * y_offset
            while x_radius > 0 and x_radius**2 + y_squared > radius_squared:
                x_radius -= 1
            width = x_radius * 2 + 1
            start_x = x - x_radius
            # lower circle half
            draw_span(start_x, y + y_offset, width)
            # upper circle half
            if y_offset != 0:
                draw_span(start_x, y - y_offset, width)
        
    
    def drawHorizontalLine(self, x, y, width, colour):
        """
        draw line on display
        x - x-coordinate of starting point
        y - y-coordinate of starting point
        width - width of horizontal line
        colour - rgb tuple
        """
        self.fillRectangle(x, y, width, 1, colour)
        
    def drawVerticalLine(self, x, y, height, colour):
        """
        draw line on display
        x - x-coordinate of starting point
        y - y-coordinate of starting point
        width - width of horizontal line
        colour - rgb tuple
        """
        self.fillRectangle(x, y, 1, height, colour)
        
    def drawLine(self, x1, y1, x2, y2, colour):
        """
        draw line on display
        x1 - x-coordinate of starting point
        y1 - y-coordinate of starting point
        x2 - x-coordinate of end point
        y2 - y-coordinate of end point
        colour - rgb tuple
        """
        # horizontal line
        if y1 == y2:
            self.drawHorizontalLine(min(x1, x2), y1, abs(x2 - x1) + 1, colour)
            return
        # vertical line
        if x1 == x2:
            self.drawVerticalLine(x1, min(y1, y2), abs(y2 - y1) + 1, colour)
            return
        # diagonal line
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        error = dx - dy
        
        while True:
            self.drawPixel(x1, y1, colour)
            if x1 == x2 and y1 == y2:
                break
            error2 = 2*error
            if error2 > -dy:
                error -= dy
                x1 += sx
            if error2 < dx:
                error += dx
                y1 += sy


    def drawCircle(self, x_cent, y_cent, radius, colour):
        """
        draw circle outline on display
        x - x-coordinate of center
        y - y-coordinate of center
        radius - radius of circle
        colour - rgb tuple
        """
        conv_col = self.convertColour(colour)
        def plotCirclePoints(cx, cy, x, y):
            self.setWindow(cx + x + self.offset[0], cy + y + self.offset[1], cx + x + 1, cy + y + 1)
            self.send(self.RAMWR, [conv_col >> 8, conv_col])
            self.setWindow(cx - x + self.offset[0], cy + y + self.offset[1], cx - x + 1, cy + y + 1)
            self.send(self.RAMWR, [conv_col >> 8, conv_col])
            self.setWindow(cx + x + self.offset[0], cy - y + self.offset[1], cx + x + 1, cy - y + 1)
            self.send(self.RAMWR, [conv_col >> 8, conv_col])
            self.setWindow(cx - x + self.offset[0], cy - y + self.offset[1], cx - x + 1, cy - y + 1)
            self.send(self.RAMWR, [conv_col >> 8, conv_col])
            if x != y:
                self.setWindow(cx + y + self.offset[0], cy + x + self.offset[1], cx + y + 1, cy + x + 1)
                self.send(self.RAMWR, [conv_col >> 8, conv_col])
                self.setWindow(cx - y + self.offset[0], cy + x + self.offset[1], cx - y + 1, cy + x + 1)
                self.send(self.RAMWR, [conv_col >> 8, conv_col])
                self.setWindow(cx + y + self.offset[0], cy - x + self.offset[1], cx + y + 1, cy - x + 1)
                self.send(self.RAMWR, [conv_col >> 8, conv_col])
                self.setWindow(cx - y + self.offset[0], cy - x + self.offset[1], cx - y + 1, cy - x + 1)
                self.send(self.RAMWR, [conv_col >> 8, conv_col])
        x = radius
        y = 0
        p = 1 - radius
        plotCirclePoints(x_cent, y_cent, x, y)
        if radius == 0:
            return
        plotCirclePoints(x_cent, y_cent, radius, 0)
        while x > y:
            y += 1
            if p <= 0:
                p = p + 2*y + 1
            else:
                x -= 1
                p = p + 2*y - 2*x + 1 
            plotCirclePoints(x_cent, y_cent, x, y)


    def turnOff(self):
        """
        turn off display
        """
        self.send(self.DISPOFF, [])
        
        
    def turnOn(self):
        """
        turn on display
        """
        self.send(self.DISPON, [])
    
    
    def print(self, text, x, y, textColour, bgColour, size=1):
        """
        print String on display
        x - x-coordinate of starting point
        y - y-coordinate of starting point
        textColour - rgb tuple for the text colour
        bgColour - rgb tuple for the background colour
        size - size of text
        """
        conv_textCol = self.convertColour(textColour)
        conv_bgCol = self.convertColour(bgColour)
        hTextCol = (conv_textCol >> 8) % 256
        lTextCol = conv_textCol % 256
        hBgCol = (conv_bgCol >> 8) % 256
        lBgCol = conv_bgCol % 256
        
        for stringPos in range(len(text)):
            charAtIndex = ord(text[stringPos])
            if charAtIndex < 20: unicode = self.fontOne[charAtIndex]
            elif charAtIndex < 40: unicode = self.fontTwo[charAtIndex - 20]
            elif charAtIndex < 60: unicode = self.fontThree[charAtIndex - 40]
            elif charAtIndex < 80: unicode = self.fontFour[charAtIndex - 60]
            elif charAtIndex < 100: unicode = self.fontFive[charAtIndex - 80]
            elif charAtIndex < 120: unicode = self.fontSix[charAtIndex - 100]
            elif charAtIndex < 140: unicode = self.fontSeven[charAtIndex - 120]
            
            self.setWindow(x + stringPos * 5 * size, y, x + stringPos * 5 * size + 5 * size - 1, y + 5 * size -1)
            self.enterDataMode()
            
            for Yindex in range(5):
                for sz1 in range(size):
                    for Xindex in range(5):
                        colsel = unicode & (1 << (Yindex + Xindex * 5))
                        for sz2 in range(size):
                            if colsel != 0:
                                self.spi.write(bytearray([hTextCol]))
                                self.spi.write(bytearray([lTextCol]))
                            else:
                                self.spi.write(bytearray([hBgCol]))
                                self.spi.write(bytearray([lBgCol]))
            self.exitDataMode()