"""Module that tests owner login functionality"""
import json
import pytest

login_credentions = [
    (dict(), 400, b"Key user_name not found"),
    (dict(user_name="semainda"), 400, b"Key password not found"),
    (dict(
        user_name="semainda",
        password="ahfjhf"), 401, b"Incorrect username or password"),
    (dict(
        user_name="semainda",
        password="mk911212"), 201, b"Holaa! You Logged in as semainda.")
]
@pytest.mark.parametrize("owner_data, resp_code, msg", login_credentions)
def test_store_owner_login(test_client, owner_data, resp_code, msg):
    response = test_client.post(
        "api/v1/auth/login", data=json.dumps(owner_data),
        headers={"content-type": "application/json"})
    assert response.status_code == resp_code
    assert msg in response.data
