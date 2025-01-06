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

    def set_lights(self, black, green, red, blue):
        """
        Set the lights
        :param bool or null black:
        :param green:
        :param red:
        :param blue:
        :return:
        """

        if(self._sleeping):
            return

        if(black is not None):
            GPIO.output(self.POSITION_FOUR_LED_PIN, GPIO.HIGH if black else GPIO.LOW)
        if(green is not None):
            GPIO.output(self.POSITION_THREE_LED_PIN, GPIO.HIGH if green else GPIO.LOW)
        if(red is not None):
            GPIO.output(self.POSITION_TWO_LED_PIN, GPIO.HIGH if red else GPIO.LOW)
        if(blue is not None):
            GPIO.output(self.POSITION_ONE_LED_PIN, GPIO.HIGH if blue else GPIO.LOW)

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

    def display_bins(self, bins):
        pins: list[int] = []

        for b in bins.bins:
            if b.position == 1:
                pins.append(self.POSITION_ONE_LED_PIN)
            elif b.position == 2:
                pins.append(self.POSITION_TWO_LED_PIN)
            elif b.position == 3:
                pins.append(self.POSITION_THREE_LED_PIN)
            elif b.position == 4:
                pins.append(self.POSITION_FOUR_LED_PIN)

        self.set_lights_by_pins(pins)