import RPi.GPIO as GPIO
import time

class LdrToggle:

    BIN_1_PIN = 25
    BIN_2_PIN = 16
    BIN_3_PIN = 9
    BIN_4_PIN = 10

    _bin_1_previous = 0
    _bin_2_previous = 0
    _bin_3_previous = 0
    _bin_4_previous = 0


    def __init__(self):
        GPIO.setup(self.BIN_1_PIN, GPIO.IN)

    def get_active_bin(self) -> int or None:
        bin_1_value = self.get_light_value(self.BIN_1_PIN)
        bin_2_value = self.get_light_value(self.BIN_2_PIN)
        bin_3_value = self.get_light_value(self.BIN_3_PIN)
        bin_4_value = self.get_light_value(self.BIN_4_PIN)

        # bin_1_diff = abs(bin_1_value - self._bin_1_previous)
        # bin_2_diff = abs(bin_2_value - self._bin_2_previous)
        # bin_3_diff = abs(bin_3_value - self._bin_3_previous)
        # bin_4_diff = abs(bin_4_value - self._bin_4_previous)
        #
        # self._bin_1_previous = bin_1_value
        # self._bin_2_previous = bin_2_value
        # self._bin_3_previous = bin_3_value
        # self._bin_4_previous = bin_4_value

        ## If one bin diff is significantly greater than the others, return that bin
        bins = [bin_1_value, bin_2_value, bin_3_value, bin_4_value]
        # print(bins)
        greatest_bin = max(bins)
        next_greatest_bin = max([b for b in bins if b != greatest_bin])

        if(greatest_bin > 2 * next_greatest_bin and greatest_bin > 100):
            return bins.index(greatest_bin) + 1

        return None

    def get_light_value(self, pin):
        count = 0

        # Output on the pin for
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
        time.sleep(0.1)

        # Change the pin back to input
        GPIO.setup(pin, GPIO.IN)

        # Count until the pin goes high
        while (GPIO.input(pin) == GPIO.LOW):
            count += 1

        return count