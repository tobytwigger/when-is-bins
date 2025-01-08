from gpiozero import MotionSensor

class Movement:
    def __init__(self):
        self._pir = MotionSensor(4)

    def movement_detected(self):
        # print(self._pir.)
        print("Movement detected")
        return True