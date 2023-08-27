from flask import request
from flask_restful import Resource
from api_service.api.schemas import StockInfoSchema,StockQuerySchema,StockInfoObject,StockHistorySchema,StockStatsSchema
from api_service.extensions import db, pwd_context
from flask_jwt_extended import create_access_token
from api_service.models import User,StockCall
from flask import abort, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt, jwt_required
from api_service.config import STOCK_URL
from api_service.clients.stock import StockClient
from api_service.auth.helpers import admin_required
from sqlalchemy import desc, func

class Login(Resource):    
    def post(self):
        json_data = request.get_json()
        username = json_data["username"]
        password = json_data["password"]

        user = db.session.execute(db.select(User).filter_by(username=username)).scalar()
        if not user:
            abort(401, "Invalid user credentials")

        valid_pwd = pwd_context.verify(password, user.password)
        if not valid_pwd:
            abort(401, "Invalid user credentials")

        access_token = create_access_token(
            username, additional_claims={"user_id": user.id, "role": user.role}
        )
        return jsonify(token=access_token)

class StockQuery(Resource):
    """
    Endpoint to allow users to query stocks
    """
    stock_client = StockClient(STOCK_URL)

    @jwt_required()
    def get(self):
        query_schema = StockQuerySchema()
        errors = query_schema.validate(request.args)
        if errors:
            abort(400, str(errors))

        stock_data = self.stock_client.get_stock(request.args["q"])
        if not stock_data:
            abort(404, "Stock not found")

        stock_info = StockInfoObject(stock_data)
        if not stock_info.quote:
            abort(404, "Stock quote not available")

        stock_call = StockCall(stock_data)
        stock_call.user_id = get_jwt()["user_id"]
        db.session.add(stock_call)
        db.session.commit()

        schema = StockInfoSchema()
        return schema.dump(stock_info)


class History(Resource):
    """
    Returns queries made by current user.
    """
    @jwt_required()
    def get(self):
        user_id = get_jwt()["user_id"]

        calls = db.session.execute(
            db.select(StockCall).filter_by(user_id=user_id)
        ).scalars()
        schema = StockHistorySchema(many=True)
        return sorted(schema.dump(calls), key=lambda x: x["date"], reverse=True)


class Stats(Resource):
    """
    Allows admin users to see which are the most queried stocks.
    """
    @admin_required()
    def get(self):
        top_symbols = db.session.execute(
            db.select(StockCall.symbol, func.count(StockCall.symbol).label("count"))
            .group_by(StockCall.symbol)
            .order_by(desc("count"))
            .limit(5)
        ).all()

        # marshmallow is being funny, so we're reordering once again
        schema = StockStatsSchema(many=True)
        return sorted(
            schema.dump(top_symbols), key=lambda x: x["times_requested"], reverse=True
        )
