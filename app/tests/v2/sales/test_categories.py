"""Module that tests categories endpoints"""
import json
import pytest
from ..get_tests_data import create_categories_data, get_categories_data,\
update_category_data 
from .. access_token import get_admin_token


@pytest.mark.run(order=4)
def test_get_created_categories_(test_client):
    access_token = get_admin_token(test_client)
    response = test_client.get(
        "api/v2/categories", headers={
            "Authorization": "Bearer {}".format(access_token)})
    assert response.status_code == 404
    assert b"'Categories' are not yet created" in response.data

@pytest.mark.run(order=5)
@pytest.mark.parametrize("cat_name, resp_code, msg", create_categories_data)
def test_create_categories(test_client, cat_name, resp_code, msg):
    access_token = get_admin_token(test_client)
    response = test_client.post(
        "api/v2/categories", data=json.dumps(
            cat_name), headers={
                "content-type": "application/json",
                "Authorization": "Bearer {}".format(access_token)}
        )
    assert response.status_code == resp_code
    assert msg in response.data


def test_get_created_categories(test_client):
    access_token = get_admin_token(test_client)
    response = test_client.get(
        "api/v2/categories", headers={
            "Authorization": "Bearer {}".format(access_token)})
    assert response.status_code == 200


@pytest.mark.parametrize("cat_id, resp_code", get_categories_data)
def test_get_specific_category(test_client, cat_id, resp_code):
    access_token = get_admin_token(test_client)
    response = test_client.get(
        "api/v2/categories/" + str(cat_id), headers={
            "Authorization": "Bearer {}".format(access_token)})
    assert response.status_code == resp_code


@pytest.mark.parametrize("cat_name, cat_id, resp_code, msg", update_category_data )
def test_update_specific_category(test_client, cat_name, cat_id, resp_code, msg):
    access_token = get_admin_token(test_client)
    response = test_client.put(
        "api/v2/categories/" + str(cat_id), data=json.dumps(cat_name), 
        headers={
            "content-type": "application/json",
            "Authorization": "Bearer {}".format(access_token)})
    assert response.status_code == resp_code
    assert msg in response.data