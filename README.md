# JoyPi Advanced Raspberry Pi Pico
 This library is a collection for the Raspberry Pi Pico for several modules on the Joy-Pi Advanced. See [here](https://www.joy-pi.net) for more information.

## Included modules
This library includes the following modules:
- ADC
- Gyroscope
- Barometer
- Button matrix
- Color Sensor - library from [`PiicoDev® Colour Sensor VEML6040 MicroPython Module`](https://github.com/CoreElectronics/CE-PiicoDev-VEML6040-MicroPython-Module)
- 16x2 LCD
- TFT 1.8
- Touchpads - library from [`MicroPython MPR121`](https://github.com/mcauser/micropython-mpr121/tree/master )
- Infrared sensor - library from [`micropython_ir`](https://github.com/peterhinch/micropython_ir/tree/master)
- 7-segment display - library from [`HT16K33 Drivers 3.5.0`](https://github.com/smittytone/HT16K33-Python/tree/main)
- RFID - library from [`micropython-mfrc522`](https://github.com/danjperron/micropython-mfrc522/tree/master)
- RTC
- OLED - library from [`micropython-ssd1306`](https://github.com/stlehmann/micropython-ssd1306/tree/master)

## Installation
Download this repository and copy the folder lib onto your Raspberry Pi Pico.

## Library Guide
### ADC
- `ADC_TLA2518(spi, cs = 17)` - initialize ADC with default values
- `begin()` - starts communication
- `read_value(channel)` - returns raw value from a selected channel
- `read_voltage(channel, value=None)` - returns measured voltage from a selected channel, raw value can also be calculated into voltage with this method
### Gyroscope
- `ICG1020S(spi, cs = 27)`- initialize gyroscope with default values
- `begin()` - starts communication
- `getTemperature()` - returns measured temperature
- `getTilt()` - returns the tilted direction
- `scale_Factor(scale)` - sets scale factor of the gyroscope (0, 8, 16 or 24)
### Barometer
- `MS5607(i2c, addr = 0x77, res = 4096)` - initialize barometer with default values
- `begin()` - starts communication
- `get_pressure()` - returns the measured pressure
- `get_temperature()`- returns the measured temperature
- `get_altitude(reference_pressure = 1013.25)` - return the calculated altitude with the measured pressure and your local pressure (`reference_pressure`)
### Button matrix
- `Buttonmatrix(i2c, addr = 0x22)`- initialize button matrix with default values
- `begin()` - starts communication
- `getKey()` - returns the pressed button
- `clearMemory()` - clears class variable `calculated`
- `calculate()` - method to use the button matrix as a calculator
### Color sensor
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
### 16x2 LCD
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
### 1.8 TFT
- `ST7735(spi, dc = 26, res = 27, cs = 10, x_offset = 2, y_offset = 1, rgbMode = "bgr")`- initialize TFT with default values
- `begin()`- starts communication
- `fillRec(x, y, width, height, colour)`- method to draw filled rectangle, where x and y are the coordinates of the left upper corner
- `fill(colour)`- fills display with one colour
- `clear()`- clears display 
- `drawPixel(x, y, colour)`- draws pixel onto the display
- `fillCircle(x, y, radius, colour)`- draws filled circle on display, where x and y are the coordinates of the center
- `drawLine(x1, y1, x2, y2, colour)`- draws line, where x1 and y1 are the coordinates of the starting point and x2 and y2 are the coordinates of the end point
- `drawCircle(x_cent, y_cent, radius, colour)`- draws circle, where x_cent and y_cent are the coordinates of the center 
- `turnOff()`- turns the display off
- `turnOn()`-  turns the display on
- `print(text, x, y, textColour, bgColour, size = 1)`- prints String onto the display, where x and y are the coordinates of the starting point
### Touchpads
- `MPR121(i2c, address = 0x5A)`- initialize touchpads with default values
- `reset()`- resets touchpads to default state
- `set_thresholds(touch, release, electrode = None)`- sets the touch and release thresholds from 0 to 255 for a single touch pad or all
- `filtered_data(electrode)`- returns filtered data value for a specific touch pad
- `baseline_electrode(electrode)`- returns baseline data value for a specific touch pad
- `touched()`- returns a 12bit value which represents which touch pad is touch and which is not (LSB)
- `is_touched(electrode)`- returns true if a specific touch pads is touched
- `get_all_states()`- returns the state of all touchpads
### Infrared sensor
- `NEC_8(pin, nedges, tblock, callback, *args)`- initialize infrared receiver for a remote controller with NEC 8 encoding (`*args` includes arguments for the callback function)
- `NEC_16(pin, nedges, tblock, callback, *args)`- initialize infrared receiver for a remote controller with NEC 16 encoding (`*args` includes arguments for the callback function)
- `NEC_SAMSUNG(pin, nedges, tblock, callback, *args)`- initialize infrared receiver for a remote controller with NEC Samsung encoding (`*args` includes arguments for the callback function)
- `do_callback(cmd, addr, ext, thresh = 0)`- sets callback method manually
- `error_function(func)`- sets a error method
- `close()`- close communication

If setting attribute `verbose` to true, the code emits debug output.
When you want to use a remote controll with a different encoding, you can add specific encodings into this directory `ir_rx` from [here](https://github.com/peterhinch/micropython_ir/tree/master/ir_rx).

**Note:** When you define your callback method, it needs to receive the arguments `data` - value from the remote, `addr` - address from remote and `ctrl` - always 0 with NEC encoding.
### 7-segment display
- `HT16K33Segment(i2c, i2c_adress=0x70)`- initialize 7-segment display with default values
- `rotate()`- rotate the segment display
- `set_colon(is_set = True)`- sets the colon of the display
- `set_glyph(glyph, digit = 0, has_dot = False)`- sets a user-defined glyph on display at a specific digit, where glyph is a 8-bit integer representing 7 segments
- `set_number(number, digit = 0, has_dot = False)`- sets single decimal value (< 10) at a specific digit
- `set_character(char, digit = 0, has_dot = False)`- sets single alpganumeric character at a specific digit
- `draw`- writes display buffer onto display 
- `printNum(num)`- write number onto the display
- `clear()`- clears display
### RFID
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
### RTC
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
### OLED
- `SSD1306_I2C(width, height, i2c, addr=0x3C, external_vcc=False)`- initialize OLED with default values
- `init_display()`- starts communication with OLED
- `poweroff()`- turns off OLED
- `poweron()`- turns on OLED
- `contrast(contrast)`- sets contrast of OLED
- `invert(invert)`- sets colour invertion
- `show()`- writes display buffer onto OLED
This library is subclassing FrameBuffer to provide for graphic primitives. Documentation can be found [here](http://docs.micropython.org/en/latest/pyboard/library/framebuf.html) for the methods to dislpay graphics.
