from screens.abstract_screen import Screen
from schedule import Scheduler, CancelJob
from database.db import Home, Bin
from data.bins import BinDayRepository
from drivers.inputs import InputEvents

from utils.state import ValueChangeNotifier

class HomeValue(ValueChangeNotifier):
    def __init__(self):
        super().__init__(self.load_home(), self.load_home)

    def load_home(self):
        return Home.get_active()

class BinConfigValue(ValueChangeNotifier):
    def __init__(self):
        super().__init__(self.load_config(), self.load_config)

    def load_config(self):
        bins = []
        for bin in Bin.select().where(Bin.home_id == Home.get_active().id):
            bins.append(bin)

        return bins

class NextBinDay(Screen):

    def __init__(self):
        self._configuration_passing = False
        self._bin_data = ValueChangeNotifier(None)
        self._visible_date = ValueChangeNotifier()
        self._home = HomeValue()
        self._bin_configuration = BinConfigValue()
        self._sleeping = ValueChangeNotifier(False)

    def schedule(self, schedule: Scheduler):
        schedule.every(30).minutes.do(self._load_bin_data)
        schedule.every(4).seconds.do(self._refresh_values)

    def _refresh_values(self):
        self._home.refresh()
        self._bin_configuration.refresh()

    def show_initial_state(self, drivers):
        drivers.lcd.display('Loading bin day', '', drivers.lcd.TEXT_STYLE_CENTER)
        self._load_bin_data()

    def _load_bin_data(self):
        self._bin_data.value = BinDayRepository(self._home.value, self._bin_configuration.value).get_bin_data()
        self._visible_date.value = self._bin_data.value.first_date()

    def handle_input(self, event: InputEvents):
        if event == InputEvents.LEFT_BUTTON_PRESSED:
            self._visible_date.value = self._bin_data.value.date_before(self._visible_date.value)
        elif event == InputEvents.RIGHT_BUTTON_PRESSED:
            self._visible_date.value = self._bin_data.value.next_date_after(self._visible_date.value)
        elif event == InputEvents.MOVEMENT_DETECTED:
            self._sleeping.value = False
        elif event == InputEvents.MOVEMENT_STOPPED:
            self._sleeping.value = True

    def tick(self, drivers):
        should_reload_data = False
        should_show = False

        if self._sleeping.handle_change():
            self._sleeping.mark_handled()
            if self._sleeping.value:
                drivers.sleep()
            else:
                drivers.wake()
                should_show = True

        if self._home.handle_change():
            should_reload_data = True

        if self._bin_data.handle_change():
            should_show = True

        if self._visible_date.handle_change():
            should_show = True

        if self._bin_configuration.handle_change():
            print('Bin configuration changed')
            should_reload_data = True

        if should_reload_data:
            self._load_bin_data()
        if should_show:
            self._show_bin_data(drivers)


    def _show_bin_data(self, drivers):
        if len(self._bin_data.value.bin_days) == 0:
            drivers.lcd.display('No data', 'available', drivers.lcd.TEXT_STYLE_CENTER)
            drivers.lights.set_lights(False, False, False, False)
            return

        date = self._visible_date.value
        if date is None:
            date = self._bin_data.value.first_date()

        bins = self._bin_data.value.get_for_date(date)

        if bins is None:
            drivers.lcd.display('No Bins', 'Found', drivers.lcd.TEXT_STYLE_CENTER)
            drivers.lights.set_lights(False, False, False, False)
        else:
            drivers.lcd.display(
                bins.date.strftime('%a, %d %b %G'),
                '',
                drivers.lcd.TEXT_STYLE_CENTER
            )

            bin_state: list[bool] = [False, False, False, False]

            for b in bins.bins:
                bin_state[b.position - 1] = True

            drivers.lights.set_lights(
                bin_state[0],
                bin_state[1],
                bin_state[2],
                bin_state[3]
            )
