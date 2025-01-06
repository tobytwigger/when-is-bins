import datetime
from uk_bin_collection.uk_bin_collection.collect_data import UKBinCollectionApp
from dataclasses import dataclass
import json
from database.db import Home, Bin

@dataclass
class BinInformation:
    """Class for a specific bin"""
    position: int
    name: str
    human_name: str

@dataclass
class BinDayInformation:
    """Class with all the bins to go out on a given day"""
    bins: list[BinInformation]
    date: datetime.date

    def push(self, bin: BinInformation):
        self.bins.append(bin)

@dataclass
class BinDayInformationCollection:
    bin_days: list[BinDayInformation]

    _visible_date: datetime.date or None

    def __init__(self, bin_days: list[BinDayInformation]):
        self.bin_days = bin_days
        self._visible_date = self.first_date()

    def first_date(self) -> datetime.date or None:
        if len(self.bin_days) == 0:
            return None
        return min([b.date for b in self.bin_days])

    def last_date(self) -> datetime.date or None:
        if len(self.bin_days) == 0:
            return None
        return max([b.date for b in self.bin_days])

    def next_date(self):
        """
        Move to the next date
        """
        next_date = False
        for b in self.bin_days:
            if b.date > self._visible_date:
                self._visible_date = b.date
                next_date = True
                break

        if next_date is False:
            self._visible_date = self.first_date()

    def previous_date(self):
        """
        Move to the previous date
        :return: bool if there is a previous date
        """
        previous_date = False
        for b in self.bin_days:
            if b.date < self._visible_date:
                self._visible_date = b.date
                previous_date = True
                break

        if previous_date is False:
            self._visible_date = self.last_date()

    def get_for_date(self, date) -> BinDayInformation or None:
        for b in self.bin_days:
            if b.date == date:
                return b

        return None

    def get_visible_date(self) -> BinDayInformation:
        return self.get_for_date(self._visible_date)

class BinDayRepository:

    def __init__(self, home: Home):
        self._home = home
        self._setup_bin_app()

    def _setup_bin_app(self):
        args = [
            self._home.council,  # Council name
            "http://example.com",  # URL to scrape
            "--postcode", "MK12 5AN",  # Postcode
            "--number", "59",  # Postcode
            "-s",
        ]

        if 'uprn' in self._home.council_data:
            args.append("-u")
            args.append(self._home.council_data['uprn'])

        self._bin_collection_api = UKBinCollectionApp()
        self._bin_collection_api.set_args(args)


    def get_bin_data(self) -> BinDayInformationCollection:
        remote_bin_data = self._bin_collection_api.run()

        json_bin_data = json.loads(remote_bin_data)

        bins_grouped_by_date = {}

        for b in json_bin_data["bins"]:
            new_bin = self._create_bin_information(b["type"])

            if(new_bin):
                day = bins_grouped_by_date.setdefault(b["collectionDate"], BinDayInformation(
                    bins=[],
                    date=datetime.datetime.strptime(b["collectionDate"], "%d/%m/%Y").date()
                ))
                day.push(new_bin)

        collection = BinDayInformationCollection(list(bins_grouped_by_date.values()))

        return collection

    def _create_bin_information(self, bin_name: str) -> BinInformation:
        bins = self._home.bins

        for b in bins:
            if b.council_name == bin_name:
                return BinInformation(b.position, b.council_name, b.name)

    def get_bin_options(self):
        remote_bin_data = self._bin_collection_api.run()

        json_bin_data = json.loads(remote_bin_data)

        bins = set()

        for b in json_bin_data["bins"]:
            bins.add(b["type"])

        return list(bins)