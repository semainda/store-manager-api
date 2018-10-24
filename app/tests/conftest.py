"""This module contains configurations that will accomodate testing"""
# Thirdparty imports
import os
import pytest
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager 
# Local imports
from app.db_config.db_setups import DataStuctures
from app import StoreManager
# from app.db_setups import create_db_tables, destroy_db_tables


@pytest.fixture(scope="module")
def test_client():
    """This function is used to initialize setting,
    acquare some resources before tests runs
    and release them when testing is done"""
    # setup

    APP = StoreManager(os.getenv("ENV_CONFIG"))
    APP = APP.create_app()
    testing_client = APP.test_client()
    # stop the flow and passes control to the tests
    yield testing_client
    # pick up here when tests are done
    with APP.app_context():
        dt = DataStuctures()
        dt.init_db()
        
