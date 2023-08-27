from flask import request
from flask_restful import Resource
from api_service.api.schemas import StockInfoSchema
from api_service.extensions import db, pwd_context
from flask_jwt_extended import create_access_token
from api_service.models import User
from flask import abort, jsonify, request


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
    def get(self):
        # TODO: Call the stock service, save the response, and return the response to the user in
        # the format dictated by the StockInfoSchema.
        data_from_service = None
        schema = StockInfoSchema()
        return schema.dump(data_from_service)


class History(Resource):
    """
    Returns queries made by current user.
    """
    def get(self):
        # TODO: Implement this method.
        pass


class Stats(Resource):
    """
    Allows admin users to see which are the most queried stocks.
    """
    def get(self):
        # TODO: Implement this method.
        pass
