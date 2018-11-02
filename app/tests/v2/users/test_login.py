"""Module that tests the default admin login"""
import json
import pytest
from ..get_tests_data import admin_login_data, attendant_login_data

@pytest.mark.parametrize("login_data, resp_code, msg", admin_login_data)
def test_admin_login(test_client, login_data, resp_code, msg):
    response = test_client.post(
        "api/v2/auth/login", data=json.dumps(login_data),
        headers={"content-type": "application/json"})
    assert response.status_code == resp_code
    assert msg in response.data


@pytest.mark.parametrize("login_data, resp_code, msg", attendant_login_data)
def test_attendant_login(test_client, login_data, resp_code, msg):
    response = test_client.post(
        "api/v2/auth/login", data=json.dumps(login_data),
        headers={"content-type": "application/json"})
    assert response.status_code == resp_code
    assert msg in response.data
