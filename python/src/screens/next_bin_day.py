from screens.abstract_screen import Screen
from schedule import Scheduler, CancelJob
from database.db import Home, Bin
from data.bins import BinDayRepository
from drivers.inputs import InputEvents
import datetime

from utils.bin_presentation import BinPresenter
from utils.state import ScreenUsingState


class NextBinDay(ScreenUsingState):


    def tick(self, drivers):
        presenter = BinPresenter(drivers, self._state)

        presenter.show(self._state.visible_date.value or datetime.date.today())

        if self._state.sleeping.handle_change():
            if self._state.sleeping.value:
                drivers.sleep()
            else:
                drivers.wake()