from drivers.buttons import Buttons
from drivers.distance import Distance
from drivers.ldr_toggle import LdrToggle
import time

class Inputs:
    _on_movement_detected = []
    _on_movement_stopped = []
    _on_left_button_pressed = []
    _on_right_button_pressed = []

    movement_timeout = 5 # seconds since last movement detected to consider movement stopped

    _movement_detected_at = None

    def __init__(self, distance: Distance, buttons: Buttons, ldr_toggle: LdrToggle):
        self._distance = distance
        self._buttons = buttons
        self._ldr_toggle = ldr_toggle

    def listen(self):
        if self._distance.movement_detected():
            if(self._movement_detected_at is None):
                for on_movement_detected in self._on_movement_detected:
                    on_movement_detected()
            self._movement_detected_at = time.time()
            time.sleep(0.5)

        if self._movement_detected_at and time.time() - self._movement_detected_at > self.movement_timeout:
            for on_movement_stopped in self._on_movement_stopped:
                on_movement_stopped()
            self._movement_detected_at = None

        if self._buttons.is_left_pressed():
            for on_left_button_pressed in self._on_left_button_pressed:
                on_left_button_pressed()
            time.sleep(0.4)

        if self._buttons.is_right_pressed():
            for on_right_button_pressed in self._on_right_button_pressed:
                on_right_button_pressed()
            time.sleep(0.4)

    def on_movement_detected(self, on_movement_detected):
        self._on_movement_detected.append(on_movement_detected)

    def on_left_button_pressed(self, on_left_button_pressed):
        self._on_left_button_pressed.append(on_left_button_pressed)

    def on_right_button_pressed(self, on_right_button_pressed):
        self._on_right_button_pressed.append(on_right_button_pressed)

    def on_movement_stopped(self, on_movement_stopped):
        self._on_movement_stopped.append(on_movement_stopped)