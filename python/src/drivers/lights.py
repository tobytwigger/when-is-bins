from threading import Thread

import RPi.GPIO as GPIO
import time
from enum import Enum

class LightState(Enum):
    OFF = 0
    ON = 1
    PHASE = 2

class Lights:
    POSITION_ONE_LED_PIN = 18
    POSITION_TWO_LED_PIN = 23
    POSITION_THREE_LED_PIN = 24
    POSITION_FOUR_LED_PIN = 25

    def __init__(self):
        GPIO.setup(self.POSITION_FOUR_LED_PIN, GPIO.OUT)
        GPIO.setup(self.POSITION_THREE_LED_PIN, GPIO.OUT)
        GPIO.setup(self.POSITION_ONE_LED_PIN, GPIO.OUT)
        GPIO.setup(self.POSITION_TWO_LED_PIN, GPIO.OUT)

        self._sleeping = False
        self._current_display = None
        self._pins_phasing = []
        self._phasing_thread = None

        self.all_off()

    def set_light_to_state(self, pin: int, state: LightState):
        if state == LightState.ON:
            GPIO.output(pin, GPIO.HIGH)
            # Remove from self._pins_phasing
            self._pins_phasing = [x for x in self._pins_phasing if x != pin]
        elif state == LightState.OFF:
            GPIO.output(pin, GPIO.LOW)
            # Remove from self._pins_phasing
            self._pins_phasing = [x for x in self._pins_phasing if x != pin]
        elif state == LightState.PHASE:
            self._pins_phasing.append(pin)

    def set_lights(self, one: LightState, two: LightState, three: LightState, four: LightState):
        if self._sleeping:
            return

        if self.cached(one, two, three, four):
            return

        self.set_light_to_state(self.POSITION_ONE_LED_PIN, one)
        self.set_light_to_state(self.POSITION_TWO_LED_PIN, two)
        self.set_light_to_state(self.POSITION_THREE_LED_PIN, three)
        self.set_light_to_state(self.POSITION_FOUR_LED_PIN, four)

        if len(self._pins_phasing) > 0:
            self._start_phasing()
        else:
            self._stop_phasing()

    def cached(self, one, two, three, four):
        cache = [one, two, three, four]

        if(self._current_display is not None and self._current_display == cache):
            return True

        self._current_display = cache

        return False

    def sleep(self):
        if self._sleeping:
            return
        self.all_off()
        self._sleeping = True

    def wake(self):
        if(not self._sleeping):
            return
        self._sleeping = False

    def cleanup(self):
        self.all_off()

    def all_off(self):
        self.set_lights(LightState.OFF, LightState.OFF, LightState.OFF, LightState.OFF)

    def _start_phasing(self):
        self._phasing_thread = Thread(target=self._phase)
        self._phasing_thread.start()

    def _phase(self):
        # Set up the PWM for the pins
        pwms = []
        for pin in self._pins_phasing:
            pwms.append(GPIO.PWM(pin, 100))

        # Start them all
        for pwm in pwms:
            pwm.start(0)

        pause_time = 0.02

        while True:
            for i in range(0, 101):
                for pwm in pwms:
                    pwm.ChangeDutyCycle(i)
                if len(self._pins_phasing) == 0:
                    break
                time.sleep(pause_time)
            for i in range(100, -1, -1):
                for pwm in pwms:
                    pwm.ChangeDutyCycle(i)
                if len(self._pins_phasing) == 0:
                    break
                time.sleep(pause_time)

            if len(self._pins_phasing) == 0:
                break

        for pwm in pwms:
            pwm.stop()


    def _stop_phasing(self):
        if self._phasing_thread is not None:
            self._pins_phasing = []
            self._phasing_thread.join()
            self._phasing_thread = None