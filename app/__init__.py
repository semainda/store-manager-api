"""Module that creates the flask app with given env"""
# thirdparty imports
from flask import Flask

# local imports
from instance.config import APP_ENV_CONFIG


def create_app(config):
    """Function that instantiate flask app with a given config"""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(APP_ENV_CONFIG[config])
    return app
