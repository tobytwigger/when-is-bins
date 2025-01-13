from screens.abstract_screen import Screen
from schedule import Scheduler, CancelJob
from database.db import Home, Bin
from data.bins import BinDayRepository
from drivers.inputs import InputEvents
import datetime
from utils.state import ValueChangeNotifier, State, ScreenUsingState, HomeValue, BinConfigValue


class SelectedBin(ScreenUsingState):

    def __init__(self, state: State = None, bin_id: int = None, date: datetime.date = None):
        super().__init__(state)
        self._bin_id = bin_id
        self._date = date

    def handle_input(self, event: InputEvents):
        if event == InputEvents.LEFT_BUTTON_PRESSED:
            self._state.visible_date.value = self._state.bin_data.value.date_before(self._state.visible_date.value)
        elif event == InputEvents.RIGHT_BUTTON_PRESSED:
            self._state.visible_date.value = self._state.bin_data.value.next_date_after(self._state.visible_date.value)
        elif event == InputEvents.MOVEMENT_DETECTED:
            self._state.sleeping.value = False
        elif event == InputEvents.MOVEMENT_STOPPED:
            self._state.sleeping.value = True
        elif event == InputEvents.BIN_1_PRESSED or event == InputEvents.BIN_2_PRESSED or event == InputEvents.BIN_3_PRESSED or event == InputEvents.BIN_4_PRESSED:
            self._state.selected_bin.value = None

    def tick(self, drivers):
        drivers.lcd.display('Selected Bin', '', drivers.lcd.TEXT_STYLE_CENTER)

        # if self._sleeping.handle_change():
        #     self._sleeping.mark_handled()
        #     if self._sleeping.value:
        #         drivers.sleep()
        #     else:
        #         drivers.wake()
        #         should_show = True
        #
        # if self._home.handle_change():
        #     should_reload_data = True
        #
        # if self._bin_data.handle_change():
        #     should_show = True
        #
        # if self._visible_date.handle_change():
        #     should_show = True
        #
        # if self._bin_configuration.handle_change():
        #     should_reload_data = True
        #
        # if self._selected_bin.handle_change():
        #     self._visible_date.value = None
        #     should_show = True
        #
        # if should_reload_data:
        #     self._load_bin_data()
        #
        # if should_show:
        #     self._show_bin_data(drivers)


    def _show_bin_data(self, drivers):
        if len(self._bin_data.value.bin_days) == 0:
            drivers.lcd.display('No data', 'available', drivers.lcd.TEXT_STYLE_CENTER)
            drivers.lights.set_lights(False, False, False, False)
            return

        if self._selected_bin.value is not None:
            # Get the name of the selected bin
            bin = None

            for b in self._bin_configuration.value:
                if b.position == self._selected_bin.value:
                    bin = b
                    break

            if bin is None:
                self._show_bin_not_found(drivers)
            else:
                # Change the visible date
                dates = self._bin_data.value.get_dates_for_bin(bin.id)

                if len(dates) > 0 and (self._visible_date.value is None or self._visible_date.value not in dates):
                    self._visible_date.value = dates[0]

                if self._visible_date.value is None:
                    self._show_bin_not_found(drivers)
                else:
                    # Check the dates array to see if we have a date that occurs after the visible date
                    has_next_date = dates.index(self._visible_date.value) < len(dates) - 1
                    has_previous_date = dates.index(self._visible_date.value) > 0
                    self._show_single_bin(drivers, bin, self._visible_date.value, has_next_date, has_previous_date)

        else:
            date = self._visible_date.value
            if date is None:
                date = self._bin_data.value.first_date()

            bins = self._bin_data.value.get_for_date(date)
            has_next_date = self._bin_data.value.next_date_after(date) is not None
            has_previous_date = self._bin_data.value.date_before(date) is not None

            if bins is None:
                self._show_empty_bins(drivers)
            else:
                self._show_all_bins(drivers, bins, has_next_date, has_previous_date)

    def _show_empty_bins(self, drivers):
        drivers.lcd.display('No Bins', 'Found', drivers.lcd.TEXT_STYLE_CENTER)
        drivers.lights.set_lights(False, False, False, False)

    def _show_bin_not_found(self, drivers):
        drivers.lcd.display('No Bin', 'Found', drivers.lcd.TEXT_STYLE_CENTER)
        drivers.lights.set_lights(False, False, False, False)

    def _show_single_bin(self, drivers, bin, date, has_next_date, has_previous_date):
        drivers.lcd.display(
            date.strftime('%a, %d %b'),
            bin.name,
            drivers.lcd.TEXT_STYLE_CENTER,
            prefix='<' if has_previous_date else None,
            suffix='>' if has_next_date else None
        )

        bin_state: list[bool] = [False, False, False, False]

        bin_state[bin.position - 1] = True

        drivers.lights.set_lights(
            bin_state[0],
            bin_state[1],
            bin_state[2],
            bin_state[3]
        )

    def _show_all_bins(self, drivers, bins, has_next_date, has_previous_date):
        print(bins)
        num_of_days_until_bins_date = (bins.date - datetime.date.today()).days
        drivers.lcd.display(
            bins.date.strftime('%a, %d %b'),
            'In ' + str(num_of_days_until_bins_date) + ' ' + ('day' if num_of_days_until_bins_date == 1 else 'days'),
            drivers.lcd.TEXT_STYLE_CENTER,
            prefix='<' if has_previous_date else None,
            suffix='>' if has_next_date else None
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