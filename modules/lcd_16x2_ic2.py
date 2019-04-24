#########################################
# HD44780 I2C class, based on Code from
# David Hilowitz
# https://github.com/dhilowitz/SamplerBox/blob/master/samplerbox.py
#########################################
import smbus
import time

# Set to True to use a 16x2 display via I2C										# Define some device parameters
USE_I2C_16X2DISPLAY = False
I2C_16x2DISPLAY_ADDR = 0x3f 			# I2C device address
I2C_16x2DISPLAY_LCD_WIDTH = 16   		# Maximum characters per line

# Define some device constants
LCD_CHR = 1  # Mode - Sending data
LCD_CMD = 0  # Mode - Sending command

LCD_LINE_1 = 0x80  # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0  # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94  # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4  # LCD RAM address for the 4th line

LCD_BACKLIGHT = 0x08  # On
# LCD_BACKLIGHT = 0x00  # Off

ENABLE = 0b00000100  # Enable bit

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005


class HD44780_I2C:
    def __init__(self):
        self.bus = smbus.SMBus(1)   # using I2C
        self.lcd_byte(0x33, LCD_CMD)  # 110011 Initialise
        self.lcd_byte(0x32, LCD_CMD)  # 110010 Initialise
        self.lcd_byte(0x06, LCD_CMD)  # 000110 Cursor move direction
        self.lcd_byte(0x0C, LCD_CMD)  # 001100 Display On,Cursor Off, Blink Off
        # 101000 Data length, number of lines, font size
        self.lcd_byte(0x28, LCD_CMD)
        self.lcd_byte(0x01, LCD_CMD)  # 000001 Clear display
        time.sleep(E_DELAY)

    def lcd_byte(self, bits, mode):
        # Send byte to data pins
        # bits = the data
        # mode = 1 for data
        #        0 for command
        bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
        bits_low = mode | ((bits << 4) & 0xF0) | LCD_BACKLIGHT

        # High bits
        self.bus.write_byte(I2C_16x2DISPLAY_ADDR, bits_high)
        self.lcd_toggle_enable(bits_high)

        # Low bits
        self.bus.write_byte(I2C_16x2DISPLAY_ADDR, bits_low)
        self.lcd_toggle_enable(bits_low)

    def lcd_toggle_enable(self, bits):
        # Toggle enable
        time.sleep(E_DELAY)
        self.bus.write_byte(I2C_16x2DISPLAY_ADDR, (bits | ENABLE))
        time.sleep(E_PULSE)
        self.bus.write_byte(I2C_16x2DISPLAY_ADDR, (bits & ~ENABLE))
        time.sleep(E_DELAY)

    def lcd_string(self, message, line):
        if line == 1:
            line_address = LCD_LINE_1
        elif line == 2:
            line_address = LCD_LINE_2
        elif line == 3:
            line_address = LCD_LINE_3
        elif line == 4:
            line_address = LCD_LINE_4

        # Send string to display
        message = message.ljust(I2C_16x2DISPLAY_LCD_WIDTH, " ")

        self.lcd_byte(line_address, LCD_CMD)

        for i in range(I2C_16x2DISPLAY_LCD_WIDTH):
            self.lcd_byte(ord(message[i]), LCD_CHR)

    def display(self, s):
        pass
