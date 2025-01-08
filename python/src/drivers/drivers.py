class Drivers:
    def __init__(self, lcd, lights, movement, buttons, ldr_toggle):
        self.lcd = lcd
        self.lights = lights
        self.movement = movement
        self.buttons = buttons
        self.ldr_toggle = ldr_toggle

    def cleanup(self):
        self.lcd.cleanup()
        self.lights.cleanup()

    def sleep(self):
        self.lcd.sleep()
        self.lights.sleep()

    def wake(self):
        self.lcd.wake()
        self.lights.wake()