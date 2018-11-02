"""Module that tests roles endpoints"""
import json
import pytest
from ..get_tests_data import get_roles_data, create_roles_data,\
update_role_data, delete_role_data
from .. access_token import get_admin_token


def test_get_roles(test_client):
    access_token = get_admin_token(test_client)
    response = test_client.get(
        "api/v2/roles", headers={
            "Authorization": "Bearer {}".format(access_token)})
    assert response.status_code == 200


@pytest.mark.parametrize("role_id, resp_code", get_roles_data)
def test_get_specific_store_role(test_client, role_id, resp_code):
    access_token = get_admin_token(test_client)
    response = test_client.get(
        "api/v2/roles/" + str(role_id), headers={
            "Authorization": "Bearer {}".format(access_token)})
    assert response.status_code == resp_code

@pytest.mark.run(order=1)
@pytest.mark.parametrize("role_name, resp_code, msg", create_roles_data)
def test_create_roles(test_client, role_name, resp_code, msg):
    access_token = get_admin_token(test_client)
    response = test_client.post(
        "api/v2/roles", data=json.dumps(
            role_name), headers={
                "content-type": "application/json",
                "Authorization": "Bearer {}".format(access_token)}
        )
    assert response.status_code == resp_code
    assert msg in response.data


@pytest.mark.parametrize("role_name, role_id, resp_code, msg", update_role_data)
def test_update_role(test_client, role_name, role_id, resp_code, msg):
    access_token = get_admin_token(test_client)
    response = test_client.put(
        "api/v2/roles/" + str(role_id), data=json.dumps(role_name), 
        headers={
            "content-type": "application/json",
            "Authorization": "Bearer {}".format(access_token)})
    assert response.status_code == resp_code
    assert msg in response.data


@pytest.mark.parametrize("role_id, resp_code, msg", delete_role_data)
def test_delete_role(test_client, role_id, resp_code, msg):
    access_token = get_admin_token(test_client)
    response = test_client.delete(
        "api/v2/roles/" + str(role_id), headers={
            "Authorization": "Bearer {}".format(access_token)})
    assert response.status_code == resp_code
    assert msg in response.data