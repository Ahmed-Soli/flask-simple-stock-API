# encoding: utf-8

from flask import request,abort
from flask_restful import Resource

from stock_service.api.schemas import StockSchema,StockQuerySchema
from stock_service.clients.stooq import StooqClient
from stock_service.config import STOOQ_URL

class StockResource(Resource):
    """
    Endpoint that is in charge of aggregating the stock information from external sources and returning
    them to our main API service. Currently we only get the data from a single external source:
    the stooq API.
    """
    stooq_client = StooqClient(STOOQ_URL)

    def get(self):
        query_schema = StockQuerySchema()
        errors = query_schema.validate(request.args)
        if errors:
            abort(400, str(errors))

        stock_data = self.stooq_client.get_stock(request.args["q"])
        if not stock_data:
            abort(404, "Stock not found")

        schema = StockSchema()
        return schema.dump(stock_data)
