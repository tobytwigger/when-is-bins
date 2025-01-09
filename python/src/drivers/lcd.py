from RPLCD.gpio import CharLCD
import RPi.GPIO as GPIO

class Lcd:
    LCD_E_PIN = 3
    LCD_RS_PIN = 2
    LCD_D4_PIN = 4
    LCD_D5_PIN = 17
    LCD_D6_PIN = 27
    LCD_D7_PIN = 22
    LCD_BACKLIGHT_TOGGLE_PIN = 10

    LCD_WIDTH = 16

    TEXT_STYLE_LEFT = 'left'
    TEXT_STYLE_CENTER = 'center'
    TEXT_STYLE_RIGHT = 'right'

    def __init__(self):
        self._lcd_init_pins()
        self._lcd = CharLCD(pin_rs=Lcd.LCD_RS_PIN, pin_e=Lcd.LCD_E_PIN, pins_data=[Lcd.LCD_D4_PIN, Lcd.LCD_D5_PIN, Lcd.LCD_D6_PIN, Lcd.LCD_D7_PIN],
                            cols=16, rows=2, numbering_mode=GPIO.BCM)
        self._lcd.cursor_mode = 'hide'
        self._lcd.clear()
        self._lcd.cursor_pos = (0, 0)
        self._current_line_1 = None
        self._current_line_2 = None
        self._sleeping = False

    def _lcd_init_pins(self):
        GPIO.setup(self.LCD_E_PIN, GPIO.OUT)
        GPIO.setup(self.LCD_RS_PIN, GPIO.OUT)
        GPIO.setup(self.LCD_D4_PIN, GPIO.OUT)
        GPIO.setup(self.LCD_D5_PIN, GPIO.OUT)
        GPIO.setup(self.LCD_D6_PIN, GPIO.OUT)
        GPIO.setup(self.LCD_D7_PIN, GPIO.OUT)
        GPIO.setup(self.LCD_BACKLIGHT_TOGGLE_PIN, GPIO.OUT)  # Backlight enable
        GPIO.output(self.LCD_BACKLIGHT_TOGGLE_PIN, GPIO.HIGH)

    def display(self, line1, line2, style, prefix=None, suffix=None):
        if self._sleeping:
            return

        # Add padding
        if style == self.TEXT_STYLE_LEFT:
            line1 = line1.ljust(self.LCD_WIDTH, ' ')
            line2 = line2.ljust(self.LCD_WIDTH, ' ')
        elif style == self.TEXT_STYLE_CENTER:
            line1 = line1.center(self.LCD_WIDTH, ' ')
            line2 = line2.center(self.LCD_WIDTH, ' ')
        elif style == self.TEXT_STYLE_RIGHT:
            line1 = line1.rjust(self.LCD_WIDTH, ' ')
            line2 = line2.rjust(self.LCD_WIDTH, ' ')

        if prefix:
            line1 = prefix + line1[len(prefix):]
        if suffix:
            line1 = line1[:self.LCD_WIDTH - len(suffix)] + suffix

        if self._current_line_1 == line1 and self._current_line_2 == line2:
            return

        self._current_line_1 = line1
        self._current_line_2 = line2
        self._lcd.clear()
        self._lcd.cursor_mode = 'hide'
        self._lcd.write_string(line1)
        self._lcd.cursor_pos = (1, 0)
        self._lcd.write_string(line2)

    def sleep(self):
        if self._sleeping:
            return
        self._lcd.clear()
        self._lcd.cursor_mode = 'hide'
        self._current_line_1 = None
        self._current_line_2 = None
        GPIO.output(self.LCD_BACKLIGHT_TOGGLE_PIN, GPIO.LOW)
        self._sleeping = True

    def wake(self):
        if(not self._sleeping):
            return
        self._sleeping = False
        GPIO.output(self.LCD_BACKLIGHT_TOGGLE_PIN, GPIO.HIGH)
        self._lcd.cursor_mode = 'hide'

    def cleanup(self):
        self._lcd.clear()
        self._lcd.cursor_mode = 'hide'