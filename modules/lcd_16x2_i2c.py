import I2C_LCD_driver


class HD44780_I2C:
    def __init__(self, address, port):
        self. lcd = I2C_LCD_driver.lcd(address, port)

    def display(self, line1, line2):
        self.lcd.lcd_clear()
        self.lcd.lcd_display_string(line1, 1)
        self.lcd.lcd_display_string(line2, 2)
