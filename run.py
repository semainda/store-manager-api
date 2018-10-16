"""Module that run the app"""
# system imports
import os

# local imports
from app import create_app

APP_CONFIG = os.getenv("ENV_CONFIG")

APP = create_app(APP_CONFIG)

if __name__ == "__main__":
    APP.run()
