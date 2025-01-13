from drivers.lights import LightState
from screens.abstract_screen import Screen
from schedule import Scheduler, CancelJob
from database.db import Home, Bin
from data.bins import BinDayRepository
from drivers.inputs import InputEvents
import datetime

from utils.date_format import format_date
from utils.state import ValueChangeNotifier, ScreenUsingState, State


class Today(ScreenUsingState):

    def handle_input(self, event: InputEvents):
        if event == InputEvents.RIGHT_BUTTON_PRESSED:
            # Set to the first date after tomorrow
            tomorrow = datetime.date.today() + datetime.timedelta(days=1)
            self._state.visible_date.value = self._state.bin_data.value.next_date_after(tomorrow)

        super().handle_input(event)

    def tick(self, drivers):
        super().tick(drivers)

        current_date = datetime.date.today()
        bins_today = self._state.bin_data.value.get_for_date(current_date)

        if bins_today is not None:
            self.show_bins_due(drivers, current_date, bins_today)
            return

        tomorrow = current_date + datetime.timedelta(days=1)
        bins_tomorrow = self._state.bin_data.value.get_for_date(tomorrow)

        if bins_tomorrow is not None:
            self.show_bins_due(drivers, tomorrow, bins_tomorrow)
            return

        next_bins = self._state.bin_data.value.next_date_after(current_date)
        num_of_days_until_next_bins = (next_bins - current_date).days

        self.show_no_bins_due(drivers, num_of_days_until_next_bins)


    def show_bins_due(self, drivers, date, bins):

        next_bins = self._state.bin_data.value.next_date_after(date)

        bins_as_text = ''
        for b in bins.bins:
            bins_as_text += b.name + ', '

        drivers.lcd.display(
            format_date(date),
            bins_as_text,
            drivers.lcd.TEXT_STYLE_CENTER,
            suffix='>' if next_bins is not None else None,
        )

        bin_state: list[LightState] = [LightState.OFF, LightState.OFF, LightState.OFF, LightState.OFF]

        for b in bins.bins:
            # Check if we SHOULD take out the bin. Currently hardcoded to tomorrow
            is_due_out = False
            if date == datetime.date.today() + datetime.timedelta(days=1):
                ## Will also need to check if the bin has been taken out
                is_due_out = True

            bin_state[b.position - 1] = LightState.PHASE if is_due_out else LightState.ON

        drivers.lights.set_lights(
            bin_state[0],
            bin_state[1],
            bin_state[2],
            bin_state[3]
        )

        return

    def show_no_bins_due(self, drivers, days_until_next_due: int or None):
        drivers.lcd.display(
            'No bins due',
            'Next bin day in ' + str(days_until_next_due) + ' ' + ('day' if days_until_next_due == 1 else 'days'),
            drivers.lcd.TEXT_STYLE_CENTER,
            suffix='>' if days_until_next_due is not None else None,
        )

        drivers.lights.all_off()