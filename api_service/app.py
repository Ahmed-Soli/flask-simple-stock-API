# encoding: utf-8

from flask import Flask
from api_service import api
from api_service.extensions import db
from api_service.extensions import migrate
from api_service.extensions import jwt


def create_app(testing=False):
    app = Flask("api_service")
    app.config.from_object("api_service.config")

    if testing is True:
        app.config["TESTING"] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///api_service.sqlite3"
    configure_extensions(app)
    register_blueprints(app)

    return app


def configure_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)


def register_blueprints(app):
    app.register_blueprint(api.views.blueprint)
