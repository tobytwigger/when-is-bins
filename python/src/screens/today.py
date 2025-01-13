from screens.abstract_screen import Screen
from schedule import Scheduler, CancelJob
from database.db import Home, Bin
from data.bins import BinDayRepository
from drivers.inputs import InputEvents
import datetime

from utils.bin_presentation import BinPresenter
from utils.state import ValueChangeNotifier, ScreenUsingState, State


class Today(ScreenUsingState):

    def show_initial_state(self, drivers):
        current_date = datetime.date.today()
        next_bins = self._state.bin_data.value.next_date_after(current_date)

        drivers.lcd.display(
            current_date.strftime('%a, %d %b'),
            'In ' + str((next_bins - current_date).days) + ' days' if next_bins is not None else 'No more bins',
            drivers.lcd.TEXT_STYLE_CENTER
        )

    def tick(self, drivers):
        presenter = BinPresenter(drivers, self._state)

        presenter.show(datetime.date.today())

        if self._state.sleeping.handle_change():
            if self._state.sleeping.value:
                drivers.sleep()
            else:
                drivers.wake()

