import csv
from datetime import datetime

import requests


class StooqObject(object):
    def __init__(self, stooq_dict):
        self.symbol = self._get_sanitized_data(stooq_dict, "Symbol")
        self.name = self._get_sanitized_data(stooq_dict, "Name")
        self.open = self._get_sanitized_data(stooq_dict, "Open")
        self.high = self._get_sanitized_data(stooq_dict, "High")
        self.low = self._get_sanitized_data(stooq_dict, "Low")
        self.close = self._get_sanitized_data(stooq_dict, "Close")
        self.date = self._get_sanitized_data(stooq_dict, "Date")
        self.time = self._get_sanitized_data(stooq_dict, "Time")

        if self.date:
            try:
                self.date = datetime.strptime(self.date, "%Y-%m-%d").date()
            except ValueError:
                self.date = None

        if self.time:
            try:
                self.time = datetime.strptime(self.time, "%H:%M:%S").time()
            except ValueError:
                self.time = None

    def _get_sanitized_data(self, d, key):
        if key not in d:
            return None

        value = d.get(key, None)
        if value == "N/D":
            return None
        return value

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False


class StooqClient(object):
    resource_path = "q/l"

    def __init__(self, base_url):
        self.base_url = base_url

    def get_stock(self, code):
        params = {"s": code, "f": "sd2t2ohlcvn", "e": "csv", "h": ""}
        with requests.get(
            "{}{}".format(self.base_url, self.resource_path), params=params, stream=True
        ) as response:
            try:
                response.raise_for_status()

                lines = (line.decode("utf-8") for line in response.iter_lines())
                reader = csv.DictReader(lines)
                result_dict = next(reader)
                return StooqObject(result_dict)
            except (requests.exceptions.HTTPError, StopIteration):
                return None
