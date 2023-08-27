# encoding: utf-8

from sqlalchemy.ext.hybrid import hybrid_property
from api_service.extensions import db, pwd_context
from sqlalchemy.sql import func


class User(db.Model):
    """Basic user model"""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    _password = db.Column("password", db.String(255), nullable=False)
    active = db.Column(db.Boolean, default=True)
    role = db.Column(db.String(20), nullable=False)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = pwd_context.hash(value)

    def __repr__(self):
        return "<User %s>" % self.username


class StockCall(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)
    time = db.Column(db.String, nullable=False)
    open = db.Column(db.Numeric, nullable=False)
    high = db.Column(db.Numeric, nullable=False)
    low = db.Column(db.Numeric, nullable=False)
    close = db.Column(db.Numeric, nullable=False)
    call_date = db.Column(db.DateTime, nullable=False, server_default=func.now())
    user_id = db.Column(db.Integer, nullable=False)

    def __init__(self, stock_data, **kwargs):
        super().__init__(**kwargs)

        self.symbol = stock_data["symbol"]
        self.name = stock_data["name"]
        self.date = stock_data["date"]
        self.time = stock_data["time"]
        self.open = stock_data["open"]
        self.high = stock_data["high"]
        self.low = stock_data["low"]
        self.close = stock_data["close"]