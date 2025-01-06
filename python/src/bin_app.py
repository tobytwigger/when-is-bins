import schedule
import time
import threading

from inputs import Inputs
from data.bins import BinDayRepository
from drivers.lights import Lights
from drivers.lcd import Lcd
from drivers.ldr_toggle import LdrToggle
from drivers.buttons import Buttons
from drivers.distance import Distance
from database.db import Home

class BinApp:
    _stop_schedule = None or threading.Event

    def __init__(self, lcd: Lcd, lights: Lights, distance: Distance, buttons: Buttons, ldr_toggle: LdrToggle):
        self._lcd = lcd
        self._lights = lights
        self._distance = distance
        self._buttons = buttons
        self._ldr_toggle = ldr_toggle
        self._inputs = Inputs(
            distance,
            buttons,
            ldr_toggle
        )

        self._assert_configured()
        self._home = Home.get_active()

        self._setup_schedule()
        self._setup_triggers()

        self._load_bin_data()

    def _setup_schedule(self):
        schedule.every(1).hours.do(self._load_bin_data)
        schedule.every(5).seconds.do(self._check_home)

    def _check_home(self):
        self._assert_configured()

        active_home = Home.get_active()

        if(active_home is not None and active_home.id != self._home.id):
            self._home = active_home
            self._load_bin_data()

    def _setup_triggers(self):
        def on_movement_detected():
            self._lcd.wake()
            self._lights.wake()
            self._show_bin_data()

        def on_movement_stopped():
            self._lcd.sleep()
            self._lights.sleep()

        def on_left_button_pressed():
            was_changed = self._bin_data.previous_date()
            self._show_bin_data()

        def on_right_button_pressed():
            was_changed = self._bin_data.next_date()
            self._show_bin_data()

        self._inputs.on_movement_detected(on_movement_detected)
        self._inputs.on_movement_stopped(on_movement_stopped)
        self._inputs.on_left_button_pressed(on_left_button_pressed)
        self._inputs.on_right_button_pressed(on_right_button_pressed)

    def init_schedule_thread(self):
        self._stop_schedule = self._run_schedule_in_background()

    def listen_for_inputs(self):
        self._inputs.listen()

    def _run_schedule_in_background(self):
        """Continuously run, while executing pending jobs at each
        elapsed time interval.
        @return cease_continuous_run: threading. Event which can
        be set to cease continuous run. Please note that it is
        *intended behavior that run_continuously() does not run
        missed jobs*. For example, if you've registered a job that
        should run every minute and you set a continuous run
        interval of one hour then your job won't be run 60 times
        at each interval but only once.
        """
        cease_continuous_run = threading.Event()

        class ScheduleThread(threading.Thread):
            @classmethod
            def run(cls):
                while not cease_continuous_run.is_set():
                    schedule.run_pending()
                    time.sleep(1)

        continuous_thread = ScheduleThread()
        continuous_thread.start()
        return cease_continuous_run

    def _load_bin_data(self):
        self._bin_data = BinDayRepository(self._home).get_bin_data()
        self._show_bin_data()

    def _show_bin_data(self):
        if len(self._bin_data.bin_days) == 0:
            self._lcd.display('No data', 'available', self._lcd.TEXT_STYLE_CENTER)
            return
        bins = self._bin_data.get_visible_date()

        self._lcd.display_bins(self._home, bins)
        self._lights.display_bins(bins)

    def cleanup(self):
        if self._stop_schedule is not None:
            self._stop_schedule.set()
        self._lcd.cleanup()
        self._lights.cleanup()

    def say_bye(self):
        self._lcd.display('Goodbye', '', self._lcd.TEXT_STYLE_CENTER)
        time.sleep(1)

    def _assert_configured(self):
        """
        Check that the app is configured correctly.
        To be configured, we need an active home, which has at least one bin set up.
        :return:
        """

        while Home.get_active() is None:
            self._lcd.display('No home', 'configured', self._lcd.TEXT_STYLE_CENTER)
            time.sleep(5)


