from drivers.buttons import Buttons
from drivers.distance import Distance
from drivers.ldr_toggle import LdrToggle
import time

from drivers.drivers import Drivers
from enum import Enum
import time

# class syntax

class InputEvents(Enum):
    LEFT_BUTTON_PRESSED = 1
    RIGHT_BUTTON_PRESSED = 2
    MOVEMENT_DETECTED = 3
    MOVEMENT_STOPPED = 4

class Inputs:
    movement_timeout = 120 # seconds since last movement detected to consider movement stopped
    _movement_detected_at = None

    def __init__(self, drivers: Drivers):
        self._drivers = drivers
        self._throttle = {}

    def listen(self):
        events = []

        if self._drivers.distance.movement_detected():
            if self._movement_detected_at is None:
                events.append(InputEvents.MOVEMENT_DETECTED)
            self._movement_detected_at = time.time()

        if self._movement_detected_at and time.time() - self._movement_detected_at > self.movement_timeout:
            events.append(InputEvents.MOVEMENT_STOPPED)
            self._movement_detected_at = None

        if self._drivers.buttons.is_left_pressed():
            if self.throttle(InputEvents.LEFT_BUTTON_PRESSED, 0.3):
                events.append(InputEvents.LEFT_BUTTON_PRESSED)

        if self._drivers.buttons.is_right_pressed():
            if self.throttle(InputEvents.RIGHT_BUTTON_PRESSED, 0.3):
                events.append(InputEvents.RIGHT_BUTTON_PRESSED)

        return events

    def throttle(self, key, timeout):
        if key in self._throttle and time.time() - self._throttle[key] < timeout:
            return False

        self._throttle[key] = time.time()
        return True
