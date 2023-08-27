from datetime import datetime

import requests


class StooqObject(object):
    def __init__(self, stooq_dict):
        self.symbol = stooq_dict.get("symbol")
        self.name = stooq_dict.get("name")
        self.open = stooq_dict.get("open")
        self.high = stooq_dict.get("high")
        self.low = stooq_dict.get("low")
        self.close = stooq_dict.get("close")
        self.date = stooq_dict.get("date")
        self.time = stooq_dict.get("time")

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


class StooqClient(object):

    def __init__(self):
        self.base_url = 'https://stooq.com/q/l'

    def get_stock(self, code):
        params = {"s": code, "f": "sd2t2ohlcvn", "e": "json", "h": ""}
        resp =  requests.get(url=self.base_url, params=params)
        try:
            resp.raise_for_status()
            json_obj = resp.json()
            #{"symbols":[{"symbol":"AAPL.US","date":"2023-08-25","time":"22:00:12","open":177.38,"high":179.15,"low":175.82,"close":178.61,"volume":51301703,"name":"APPLE"}]}
            result_dict = json_obj.get("symbols",[None])[0]            
            return StooqObject(result_dict)
        except (requests.exceptions.HTTPError, StopIteration):
            return None
