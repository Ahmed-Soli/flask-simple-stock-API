# encoding: utf-8

from api_service.extensions import ma


class StockInfoSchema(ma.Schema):
    symbol = ma.String(dump_only=True)
    company_name = ma.String(dump_only=True)
    quote = ma.Float(dump_only=True)


class StockQuerySchema(ma.Schema):
    q = ma.String(required=True)


class StockInfoObject(object):
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