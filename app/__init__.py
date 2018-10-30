"""Module that creates the flask app with given env"""
# thirdparty imports
from flask import Flask, Blueprint
from flask_restful import Api
from flask_jwt_extended import JWTManager

# local imports
from instance.config import APP_ENV_CONFIG
from .db_config.store_db_setups import DatabaseOperations

# api endpoints imports
from .api.v2.views.users import users_blueprint
from .api.v2.views.sales import sales_blueprint


class StoreManager:
    """Class that defines the flask app with given config"""

    def __init__(self, config):
        self.app = Flask(__name__, instance_relative_config=True)
        self.app.config.from_object(APP_ENV_CONFIG[config])
        # Create store database tables and default admin
        self.dt = DatabaseOperations()
        self.dt.create_db_tables(self.app.config["DATABASE_URL"])

        # blueprint rgistration
        self.app.register_blueprint(users_blueprint)
        self.app.register_blueprint(sales_blueprint)
        # initialize JWTManager
        JWTManager(self.app)

    def create_app(self):
        """Method that instantiate flask app with a given config"""
        return self.app

