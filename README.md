# JoyPi Advanced Raspberry Pi Pico
 This library is a collection for the Raspberry Pi Pico for several modules on the Joy-Pi Advanced. See [here](https://www.joy-pi.net) for more information.

## Necessary libraries for the Joy-Pi Advanced
> [!NOTE]
> This repository includes all necessary libraries which are needed for the Joy-Pi Advanced with the Raspberry Pi Pico.
> Libraries from other authors are marked as such.

| Repository | Needed for |
|---|---|
| `ADC_TLA2518` | Library to use the Analog-Digital-Converter |
| `ICG1020S` | Library to use the gyroscope |
| `MCP23008` | Library to use the buton matrix |
| `I2CLCD` | Library to use the 16x2 LCD |
| `ST7735` | Library to use the 1.8" TFT display|
| `DS1307Z` | Library to use the real time clock |
| `MS5607` | Library to use the barometer |
| `RGB_Matrix` | Library to use the RGB LED matrix on Joy-Pi Advanced 2 - RP2040 is used to communicate with led matrix|
| [`VEML6040`](https://github.com/CoreElectronics/CE-PiicoDev-VEML6040-MicroPython-Module) | Library to use the colour sensor|
| [`MPR121`](https://github.com/mcauser/micropython-mpr121/tree/master) | Library to use the touchpads |
| [`IR_RX`](https://github.com/peterhinch/micropython_ir/tree/master) | Library to use the infrared sensor |
| [`HT16K33Segment`](https://github.com/smittytone/HT16K33-Python/tree/main) | Library to use the 7-segment display |
| [`MFRC522`](https://github.com/danjperron/micropython-mfrc522/tree/master) | Library to use the RFID module|
| [`SSD1306`](https://github.com/stlehmann/micropython-ssd1306/tree/master) | Library to use the OLED display|

## Installation
Download this repository and copy the folder lib onto your Raspberry Pi Pico.

## Library Guide
### `ADC_TLA2518`
- `ADC_TLA2518(spi, cs = 17)` - initialize ADC with default values
- `begin()` - starts communication
- `read_value(channel)` - returns raw value from a selected channel
- `read_voltage(channel, value=None)` - returns measured voltage from a selected channel, raw value can also be calculated into voltage with this method

### `ICG1020S`
- `ICG1020S(spi, cs = 27)`- initialize gyroscope with default values
- `begin()` - starts communication
- `getTemperature()` - returns measured temperature
- `getTilt()` - returns the tilted direction
- `scale_Factor(scale)` - sets scale factor of the gyroscope (0, 8, 16 or 24)

### `MS5607`
- `MS5607(i2c, addr = 0x77, res = 4096)` - initialize barometer with default values
- `begin()` - starts communication
- `get_pressure()` - returns the measured pressure
- `get_temperature()`- returns the measured temperature
- `get_altitude(reference_pressure = 1013.25)` - return the calculated altitude with the measured pressure and your local pressure (`reference_pressure`)

### `MCP23008`
- `Buttonmatrix(i2c, addr = 0x22)`- initialize button matrix with default values
- `begin()` - starts communication
- `getKey()` - returns the pressed button
- `clearMemory()` - clears class variable `calculated`
- `calculate()` - method to use the button matrix as a calculator

### `I2CLCD`
- `I2CLCD(i2c, addr = 0x21)`- initialize 16x2 LCD with default values
- `begin()`- starts communication
- `clear()`- clears LCD
- `setHome()`- sets cursor to position (0,0)
- `shiftToLeft()`- shift the whole display to the left
- `shiftToRight()`- shift the whole display to the right
- `showCursor()`- show cursor
- `blinkingCursor()`- activate the blinking cursor
- `hideCursor()`- hide cursor
- `turnOff()`- turn background light off
- `turnOn()`- turn background light on
- `setCursor(x, y)`- set cursor to position (x, y)
- `print(text)`- print String onto the LCD at the current cursor position

### `ST7735`
- `ST7735(spi, dc = 26, res = 27, cs = 10, x_offset = 2, y_offset = 1, rgbMode = "bgr")`- initialize TFT with default values
- `begin()`- starts communication
- `fillRectangle(x, y, width, height, colour)`- method to draw filled rectangle, where x and y are the coordinates of the left upper corner
- `drawRectangle(x, y, width, height, colour)` - method to draw outline of a rectangle, where x and y are the coordinates of the left upper corner
- `fillTriangle(x0, y0, x1, y1, x2, y2, colour)` - method to draw triangle, where x0 and y0 are the coordinates of the left corner, x1 and y1 the coordinates of the corner in the middle and x2 and y2 the coordinates of the right cornern
- `fill(colour)`- fills display with one colour
- `clear()`- clears display 
- `drawPixel(x, y, colour)`- draws pixel onto the display
- `fillCircle(x, y, radius, colour)`- draws filled circle on display, where x and y are the coordinates of the center
- `drawLine(x1, y1, x2, y2, colour)`- draws line, where x1 and y1 are the coordinates of the starting point and x2 and y2 are the coordinates of the end point
- `drawHorizontalLine(x, y, width, colour)` - draws a horizontal line starting at the coordinates x and y and is `width` pixel long
- `drawVerticalLine(x, y, height, colour)`- draws a vertical line starting at the coordinates x and y and is `height` pixel long
- `drawCircle(x_cent, y_cent, radius, colour)`- draws circle, where x_cent and y_cent are the coordinates of the center 
- `turnOff()`- turns the display off
- `turnOn()`-  turns the display on
- `print(text, x, y, textColour, bgColour, size = 1)`- prints String onto the display, where x and y are the coordinates of the starting point

### `DS1307Z`
- `DS1307Z(i2c, addr = 0x68)`- initialize RTC with default values
- `setDate(year, month, day, weekday, hour, minute, second)`- set all values of the RTC
- `setYear(year)`- set year on the RTC
- `setMonth(month)`- set month on the RTC
- `setDay(day)`- set day on the RTC
- `setWeekday(weekday)`- set weekday on the RTC (0 - Sunday etc.)
- `setHour(hour)`- set hour on the RTC
- `setMinute(minute)`- set minute on the RTC
- `setSecond(second)`- set second on the RTC
- `getDate()`- returns all values of the RTC
- `getYear()`- returns year from the RTC
- `getMonth()`- returns month of the RTC
- `getDay()`- returns day of the RTC
- `getWeekday()`- returns weekday of the RTC
- `getHour()`- returns hour of the RTC
- `getMinute()`- returns minute of the RTC
- `getSecond()`- returns second of the RTC

### `RGB_Matrix`
- `RGB_Matrix(i2c, i2c_adress = 0x66, count = 64, brightness = 80, right_border = [7,15,23,31,39,47,55,63], left_border = [0,8,16,24,32,40,48,56]))` - initialize RGB LED matrix with already Joy-Pi Advanced values set as default
- `clean()` - turn off all pixels
- `setPixel(position, colour)` - set a pixel at `position` to `colour` (32 bit integer or tuple)
- `setBrightness(brightness)` - set brightness of led matrix to a certain level (0-255)
- `getPixelNum()` - returns number of pixels at matrix
- `RGB_on(colour)` - set all pixel of matrix to `colour` (32 bit integer or tuple)
- `RGB_off()` - turn off all pixels
- `wheel(pos)` - generate rainbow colours over `pos` positions 0-255
- `rainbow(wait_ms=20, iterations=1)` - play rainbow effect on all LEDs, where `wait_ms`is the time in bewteen colour change and `iterations` the number of repetitions
- `colourWipe(color, wait_ms=50)` - Move colours pixel by pixel over the LEDs with a given `colour` (32 bit integer or tuple), where `wait_ms`is the time in bewteen colour change
- `theaterChase(color, wait_ms=50, iterations=10)` - chaser animation with a given `colour` (32 bit integer or tuple), where `wait_ms`is the time in bewteen colour change and `iterations` the number of repetitions
- `demo1()` - simple demo programm
- `demo2()` - more complex demo programm in a continuous loop
- `show()` - show changes on LED matrix

#### `RGBW`
> [!NOTE]
> This object is for an easier and more flexible use of colour codes. 
> You can use the hexadecimal value, separate RGB values or separate RGBW values.
- `RGBW(r, g=None, b=None, w=None)`- create new RGBW value in two possible ways: 
    1. with a single integer `RGBW(0xWWRRGGBB)`as parameter `r`
    2. with individual colour components as a tuple `(r, g, b, w=0)`
- `unpackRGBW()` - returns value of `RGBW`- object as colour tuple `(red, green, blue, white)`
- `unpackHEX()`- return value of `RGBW`- object as 32 bit integer `0xWWRRGGBB`

### [`VEML6040`](https://github.com/CoreElectronics/CE-PiicoDev-VEML6040-MicroPython-Module)
- `VEML6040(i2c, address = 0x10)`- initialize colour sensor with default values
- `enableSensor()` - start communication
- `disableSensor()`- end communication
- `setIntegrationTime()` - set integration time (`0`-40ms, `1`-80ms, `2`-160ms, `3`-320ms, `4`-640ms or `5`-1280ms)
- `forceMode()` - forces measurement mode
- `autoMode()`- automatic measurement mode
- `get_red()`- returns the raw value of red
- `get_green()`- returns the raw value of green
- `get_blue()`- returns the raw value of blue
- `get_white()`- returns the raw value of white
- `get_rgbw()`- returns all raw values of RGBW
- `readAll()` - returns most recognized RGB colour as well as all raw values

### [`MPR121`](https://github.com/mcauser/micropython-mpr121/tree/master)
- `MPR121(i2c, address = 0x5A)`- initialize touchpads with default values
- `reset()`- resets touchpads to default state
- `set_thresholds(touch, release, electrode = None)`- sets the touch and release thresholds from 0 to 255 for a single touch pad or all
- `filtered_data(electrode)`- returns filtered data value for a specific touch pad
- `baseline_electrode(electrode)`- returns baseline data value for a specific touch pad
- `touched()`- returns a 12bit value which represents which touch pad is touch and which is not (LSB)
- `is_touched(electrode)`- returns true if a specific touch pads is touched
- `get_all_states()`- returns the state of all touchpads

### [`IR_RX`](https://github.com/peterhinch/micropython_ir/tree/master)
- `NEC_8(pin, nedges, tblock, callback, *args)`- initialize infrared receiver for a remote controller with NEC 8 encoding (`*args` includes arguments for the callback function)
- `NEC_16(pin, nedges, tblock, callback, *args)`- initialize infrared receiver for a remote controller with NEC 16 encoding (`*args` includes arguments for the callback function)
- `NEC_SAMSUNG(pin, nedges, tblock, callback, *args)`- initialize infrared receiver for a remote controller with NEC Samsung encoding (`*args` includes arguments for the callback function)
- `do_callback(cmd, addr, ext, thresh = 0)`- sets callback method manually
- `error_function(func)`- sets a error method
- `close()`- close communication
> [!NOTE]
> If setting attribute `verbose` to true, the code emits debug output.
>
> When you want to use a remote controll with a different encoding, you can add specific encodings into this directory `ir_rx` from [here](https://github.com/peterhinch/micropython_ir/tree/master/ir_rx).
> 
> When you define your callback method, it needs to receive the arguments `data` - value from the remote, `addr` - address from remote and `ctrl` - always 0 with NEC encoding.

### [`HT16K33Segment`](https://github.com/smittytone/HT16K33-Python/tree/main)
- `HT16K33Segment(i2c, i2c_adress=0x70)`- initialize 7-segment display with default values
- `rotate()`- rotate the segment display
- `set_colon(is_set = True)`- sets the colon of the display
- `set_glyph(glyph, digit = 0, has_dot = False)`- sets a user-defined glyph on display at a specific digit, where glyph is a 8-bit integer representing 7 segments
- `set_number(number, digit = 0, has_dot = False)`- sets single decimal value (< 10) at a specific digit
- `set_character(char, digit = 0, has_dot = False)`- sets single alpganumeric character at a specific digit
- `draw`- writes display buffer onto display 
- `printNum(num)`- write number onto the display
- `clear()`- clears display

### [`MFRC522`](https://github.com/danjperron/micropython-mfrc522/tree/master)
- `MFRC522(ck, mosi, miso, rst, cs,baudrate=1000000,spi_id=0)`- initialize RFID module
- `init()`- start communication
- `reset()`- reset RFID module
- `antenna_on(on = True)`- activate or deactivate antenna
- `request(mode)`- request data from RFID module in a mode (REQIDL or REQALL)
- `anticoll(anticolN)`- sets anticollision 
- `PcdSelect(serNum, anticolN)`- checks if reading of tag went smoothly
- `SelectTag(uid)`- checks if tag has a specific UID
- `tohexstring(v)`- converts hex to string
- `SelectTagSN()`- returns is reading of a tag was correct and uid
- `auth(mode, addr, sect, ser)`- check if tag can be written on 
- `authKeys(uid, addr, keyA = None, keyB = None)`- check if which key to use to write
- `stop_crypto1()`- stop encription
- `read(addr)`- returns specific block (`addr`) of tag
- `write(addr, data)`- writes into a specific block (`addr`) data
- `writeSectorBlock(uid, sector, block, data, keyA = None, keyB = None)`- write data into a specific sector and block
- `readSectorBlock(uid, sector, block, keyA = None, keyB = None)`- read data from a specific sector and block
- `MFRC522_DumpClassic1K(uid, Start = 0, End = 64, keyA = None, keyB = None)`- returns all data from tag (start and end can be defined)

### [`SSD1306`](https://github.com/stlehmann/micropython-ssd1306/tree/master)
- `SSD1306_I2C(width, height, i2c, addr=0x3C, external_vcc=False)`- initialize OLED with default values
- `init_display()`- starts communication with OLED
- `poweroff()`- turns off OLED
- `poweron()`- turns on OLED
- `contrast(contrast)`- sets contrast of OLED
- `invert(invert)`- sets colour invertion
- `show()`- writes display buffer onto OLED

> [!NOTE]
> This library is subclassing FrameBuffer to provide for graphic primitives. Documentation can be found [here](http://docs.micropython.org/en/latest/pyboard/library/framebuf.html) for the methods to dislpay graphics.