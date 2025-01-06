import RPi.GPIO as GPIO
import time

class Distance:
    DISTANCE_TRIG_PIN = 23
    DISTANCE_ECHO_PIN = 24

    _old_distance = 0

    def __init__(self):
        GPIO.setup(self.DISTANCE_TRIG_PIN, GPIO.OUT)
        GPIO.setup(self.DISTANCE_ECHO_PIN, GPIO.IN)
        GPIO.output(self.DISTANCE_TRIG_PIN, False)


    def get_distance(self):
        GPIO.output(self.DISTANCE_TRIG_PIN, True)

        time.sleep(0.00001)

        GPIO.output(self.DISTANCE_TRIG_PIN, False)

        while GPIO.input(self.DISTANCE_ECHO_PIN) == 0:
            pulse_start = time.time()

        while GPIO.input(self.DISTANCE_ECHO_PIN) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start

        distance = pulse_duration * 17150

        distance = round(distance, 2)

        return distance

    def get_distance_with_units(self):
        return str(self.get_distance()) + 'cm'

    def movement_detected(self):
        distance = self.get_distance()
        distance_diff = abs(distance - self._old_distance)

        self._old_distance = distance

        # Return true if the distance has changed by more than 20% or 50cm, whatever is greater
        if distance_diff > max(0.2 * distance, 50):
            self._old_distance = distance
            return True

        return False