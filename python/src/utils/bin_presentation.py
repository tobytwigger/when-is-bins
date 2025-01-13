class BinPresenter:
    def __init__(self, drivers, state):
        self._drivers = drivers
        self._state = state


    def show(self, date):
        print(date)
        # TODO Make this more efficient

        # Get the relevant bins
        bins = self._state.bin_data.value.get_for_date(date)

        # Get whether we can go back and/or forward
        has_next_date = self._state.bin_data.value.next_date_after(date) is not None
        has_previous_date = self._state.visible_date.value is not None

        if bins is None:
            self._show_empty_bins()
            return
        else:
            self.show_all_bins(date, bins, has_next_date, has_previous_date)

    def show_all_bins(self, date, bins, has_next_date, has_previous_date):

        print(bins)
        num_of_days_until_bins_date = (bins.date - date).days
        self._drivers.lcd.display(
            bins.date.strftime('%a, %d %b'),
            'In ' + str(num_of_days_until_bins_date) + ' ' + ('day' if num_of_days_until_bins_date == 1 else 'days'),
            self._drivers.lcd.TEXT_STYLE_CENTER,
            prefix='<' if has_previous_date else None,
            suffix='>' if has_next_date else None
        )

        bin_state: list[bool] = [False, False, False, False]

        for b in bins.bins:
            bin_state[b.position - 1] = True

        self._drivers.lights.set_lights(
            bin_state[0],
            bin_state[1],
            bin_state[2],
            bin_state[3]
        )

    def _show_empty_bins(self):
        self._drivers.lcd.display('No Bins', 'Due', self._drivers.lcd.TEXT_STYLE_CENTER)
        self._drivers.lights.set_lights(False, False, False, False)