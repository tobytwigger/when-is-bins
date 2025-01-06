#!/home/toby/when-is-bins/python/.venv/bin/python

import RPi.GPIO as GPIO
import time
import signal
from uk_bin_collection.uk_bin_collection.collect_data import UKBinCollectionApp

from drivers.lcd import Lcd
from drivers.ldr_toggle import LdrToggle
from drivers.lights import Lights
from drivers.distance import Distance
import threading
from bin_app import BinApp
from drivers.buttons import Buttons

should_kill = False

def sigterm_handler(signal, frame):
    global should_kill
    should_kill = True

def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

def run():
    signal.signal(signal.SIGTERM, sigterm_handler)

    set_up_gpio()

    lcd = Lcd()
    lights = Lights()
    distance = Distance()
    buttons = Buttons()
    ldr_toggle = LdrToggle()

    app = BinApp(
        lcd,
        lights,
        distance,
        buttons,
        ldr_toggle
    )

    app.init_schedule_thread()

    try:
        while True:
            app.listen_for_inputs()
            if should_kill:
                break
    except KeyboardInterrupt:
        # Do nothing
        pass

    app.say_bye()
    app.cleanup()
    GPIO.cleanup()
    print('clean')
    print('bye')

def set_up_gpio():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

def check_inputs(distance, on_movement):
    if distance.movement_detected():
        on_movement()

if __name__ == "__main__":
    run()

