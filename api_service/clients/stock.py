import requests


class StockObject(object):
    def __init__(self, stock_dict):
        self.symbol = stock_dict.get("symbol", None)
        self.company_name = stock_dict.get("name", None)
        self.quote = stock_dict.get("close", None)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

    def __repr__(self):
        return "StockObject (symbol={} company_name={} quote={})".format(
            self.symbol, self.company_name, self.quote
        )


class StockClient(object):
    resource_path = "api/v1/stock"

    def __init__(self, base_url):
        self.base_url = base_url

    def get_stock(self, code):
        params = {"q": code}
        response = requests.get(
            "{}{}".format(self.base_url, self.resource_path), params=params
        )
        try:
            response.raise_for_status()
            return response.json()
        except (requests.exceptions.HTTPError, requests.exceptions.JSONDecodeError):
            return None
