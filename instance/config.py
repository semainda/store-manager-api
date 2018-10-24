"""Module that holds application env configs"""
# system imports
import os, json


class Config:
    """Class that holds default env configs"""
    DEBUG = False
    DEFAULT_ADMIN = json.loads(os.environ["ADMIN_CONFIG"])
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")


class DevelopmentConfig(Config):
    """Class that holds development env configs"""
    DEBUG = True


class TestingConfig(Config):
    """Class that holds testing env configs"""
    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    """Class that holds production env configs"""
    TESTING = False


APP_ENV_CONFIG = {
    "testing": TestingConfig,
    "development": DevelopmentConfig,
    "production": ProductionConfig
}
