import RPi.GPIO as GPIO
import time

class Lights:
    POSITION_FOUR_LED_PIN = 21
    POSITION_THREE_LED_PIN = 27
    POSITION_ONE_LED_PIN = 17
    POSITION_TWO_LED_PIN = 20

    _sleeping = False

    def __init__(self):
        GPIO.setup(self.POSITION_FOUR_LED_PIN, GPIO.OUT)
        GPIO.setup(self.POSITION_THREE_LED_PIN, GPIO.OUT)
        GPIO.setup(self.POSITION_ONE_LED_PIN, GPIO.OUT)
        GPIO.setup(self.POSITION_TWO_LED_PIN, GPIO.OUT)

        self.set_lights(False, False, False, False)

    def set_lights_by_pins(self, pins: list[int]):
        """If pins includes POSITION_FOUR_LED_PIN, turn it on. Else, turn it off"""
        if(self._sleeping):
            return

        GPIO.output(self.POSITION_FOUR_LED_PIN, GPIO.HIGH if self.POSITION_FOUR_LED_PIN in pins else GPIO.LOW)
        GPIO.output(self.POSITION_THREE_LED_PIN, GPIO.HIGH if self.POSITION_THREE_LED_PIN in pins else GPIO.LOW)
        GPIO.output(self.POSITION_TWO_LED_PIN, GPIO.HIGH if self.POSITION_TWO_LED_PIN in pins else GPIO.LOW)
        GPIO.output(self.POSITION_ONE_LED_PIN, GPIO.HIGH if self.POSITION_ONE_LED_PIN in pins else GPIO.LOW)

    def set_lights(self, one, two, three, four):
        if(self._sleeping):
            return

        if(one is not None):
            GPIO.output(self.POSITION_ONE_LED_PIN, GPIO.HIGH if one else GPIO.LOW)
        if(two is not None):
            GPIO.output(self.POSITION_TWO_LED_PIN, GPIO.HIGH if two else GPIO.LOW)
        if(three is not None):
            GPIO.output(self.POSITION_THREE_LED_PIN, GPIO.HIGH if three else GPIO.LOW)
        if(four is not None):
            GPIO.output(self.POSITION_FOUR_LED_PIN, GPIO.HIGH if four else GPIO.LOW)

    def sample_lights(self):
        print('sample')
        self.set_lights(False, False, False, False)
        time.sleep(0.2)
        self.set_lights(True, False, False, False)
        time.sleep(0.2)
        self.set_lights(True, True, False, False)
        time.sleep(0.2)
        self.set_lights(True, True, True, False)
        time.sleep(0.2)
        self.set_lights(True, True, True, True)
        time.sleep(0.2)
        self.set_lights(False, True, True, True)
        time.sleep(0.2)
        self.set_lights(False, False, True, True)
        time.sleep(0.2)
        self.set_lights(False, False, False, True)
        time.sleep(0.2)
        self.set_lights(False, False, False, False)


    def sleep(self):
        if self._sleeping:
            return
        self.set_lights(False, False, False, False)
        self._sleeping = True

    def wake(self):
        if(not self._sleeping):
            return
        self._sleeping = False

    def cleanup(self):
        self.set_lights(False, False, False, False)
