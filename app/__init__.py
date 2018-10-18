"""Module that creates the flask app with given env"""
# thirdparty imports
from flask import Flask, Blueprint
from flask_restful import Api
from flask_jwt_extended import JWTManager

# local imports
from instance.config import APP_ENV_CONFIG
from .db_config.db_setups import DataStuctures

# api endpoints imports
from .api.v1.views.users.login import Login

# blueprint object
API_V1_BLUEPRINT = Blueprint("v1", __name__, url_prefix="/api/v1")
API = Api(API_V1_BLUEPRINT)


class StoreManager:
    """Class that defines the flask app with given config"""

    def __init__(self, config):
        self.app = Flask(__name__, instance_relative_config=True)
        self.app.config.from_object(APP_ENV_CONFIG[config])
         # Create store data stuctures and default administrator
        self.dt_tb = DataStuctures()
        self.dt_tb.init_db()
        self.owner = self.dt_tb.create_default_admin(
            self.app.config["DEFAULT_ADMIN"])
        print(self.owner)
        # blueprint rgistration
        self.app.register_blueprint(API_V1_BLUEPRINT)
        # user auth endpoints
        API.add_resource(Login, "/auth/login")
        # initialize JWTManager
        JWTManager(self.app)

    def create_app(self):
        """Method that instantiate flask app with a given config"""
        return self.app
