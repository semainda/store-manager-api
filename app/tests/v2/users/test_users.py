"""Module that tests users endpoints"""
import json
import pytest
from ..get_tests_data import create_users_data, get_users_data
from .. access_token import get_admin_token


@pytest.mark.run(order=2)
@pytest.mark.parametrize("user_data, resp_code, msg", create_users_data)
def test_create_users(test_client, user_data, resp_code, msg):
    access_token = get_admin_token(test_client)
    response = test_client.post(
        "api/v2/users", data=json.dumps(
            user_data), headers={
                "content-type": "application/json",
                "Authorization": "Bearer {}".format(access_token)}
        )
    assert response.status_code == resp_code
    assert msg in response.data

def test_get_users(test_client):
    access_token = get_admin_token(test_client)
    response = test_client.get(
        "api/v2/users", headers={
            "Authorization": "Bearer {}".format(access_token)})
    assert response.status_code == 200


@pytest.mark.parametrize("user_id, resp_code", get_users_data)
def test_get_specific_user(test_client, user_id, resp_code):
    access_token = get_admin_token(test_client)
    response = test_client.get(
        "api/v2/users/" + str(user_id), headers={
            "Authorization": "Bearer {}".format(access_token)})
    assert response.status_code == resp_code
