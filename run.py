"""Module that run the flask app"""
# system imports
import os

# local imports
from app import StoreManager

APP_CONFIG = os.getenv("ENV_CONFIG")

APP = StoreManager(APP_CONFIG)

if __name__ == "__main__":
    APP = APP.create_app()
    APP.run()
