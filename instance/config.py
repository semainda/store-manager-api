"""Module that holds application env configs"""
# system imports
import os, json


class Config:
    """Class that holds default env configs"""
    DEBUG = False
    DEFAULT_ADMIN = json.loads(os.getenv("ADMIN_CONFIG"))
    DEFAULT_ATTENDANT = os.getenv("STORE_ATTENDANT_ROLE")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    DATABASE_URL = os.getenv("DATABASE_URL")


class DevelopmentConfig(Config):
    """Class that holds development env configs"""
    DEBUG = True


class TestingConfig(Config):
    """Class that holds testing env configs"""
    DEBUG = True
    TESTING = True
    DATABASE_URL = os.getenv("TEST_DATABASE_URL")


class ProductionConfig(Config):
    """Class that holds production env configs"""
    TESTING = False


APP_ENV_CONFIG = {
    "testing": TestingConfig,
    "development": DevelopmentConfig,
    "production": ProductionConfig
}
