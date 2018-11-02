"""Module that tests user_roles endpoints"""
import json
import pytest
from ..get_tests_data import create_user_roles, get_user_role,\
update_users_role
from .. access_token import get_admin_token


def test_get_user_roles(test_client):
    access_token = get_admin_token(test_client)
    response = test_client.get(
        "api/v2/users/roles", headers={
            "Authorization": "Bearer {}".format(access_token)})
    assert response.status_code == 200

@pytest.mark.run(order=3)
@pytest.mark.parametrize("user_role, resp_code, msg", create_user_roles)
def test_create_user_role(test_client, user_role, resp_code, msg):
    access_token = get_admin_token(test_client)
    response = test_client.post(
        "api/v2/users/roles", data=json.dumps(user_role), 
        headers={
            "content-type": "application/json",
            "Authorization": "Bearer {}".format(access_token)})
    assert response.status_code == resp_code
    assert msg in response.data


@pytest.mark.parametrize("user_role_id, resp_code", get_user_role)
def test_get_specific_user_role(test_client, user_role_id, resp_code):
    access_token = get_admin_token(test_client)
    response = test_client.get(
        "api/v2/users/roles/" + str(user_role_id), headers={
            "Authorization": "Bearer {}".format(access_token)})
    assert response.status_code == resp_code


@pytest.mark.parametrize("role_id, user_id, resp_code, msg", update_users_role)
def test_update_user_role(test_client, role_id, user_id, resp_code, msg):
    access_token = get_admin_token(test_client)
    response = test_client.put(
        "api/v2/users/roles/" + str(user_id), data=json.dumps(role_id),
        headers={
            "content-type": "application/json",
            "Authorization": "Bearer {}".format(access_token)})
    assert response.status_code == resp_code
    assert msg in response.data