import RPi.GPIO as GPIO

class Buttons:

    LEFT_BUTTON_PIN = 7
    RIGHT_BUTTON_PIN = 12

    def __init__(self):
        GPIO.setup(self.LEFT_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.RIGHT_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def is_left_pressed(self):
        return GPIO.input(self.LEFT_BUTTON_PIN) == GPIO.HIGH

    def is_right_pressed(self):
        return GPIO.input(self.RIGHT_BUTTON_PIN) == GPIO.HIGH