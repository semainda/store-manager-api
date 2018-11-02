"""Module that tests sub_categories endpoints"""
import json
import pytest
from ..get_tests_data import create_sub_categories, get_sub_categories_data,\
update_sub_categories_data
from .. access_token import get_admin_token

@pytest.mark.run(order=6)
def test_get_created_subcategories(test_client):
    access_token = get_admin_token(test_client)
    response = test_client.get(
        "api/v2/subcategories", headers={
            "Authorization": "Bearer {}".format(access_token)})
    assert response.status_code == 404
    assert b"'SubCategories' are not yet created" in response.data

@pytest.mark.run(order=7)
@pytest.mark.parametrize("sub_name, resp_code, msg", create_sub_categories)
def test_create_subcategories(test_client, sub_name, resp_code, msg):
    access_token = get_admin_token(test_client)
    response = test_client.post(
        "api/v2/subcategories", data=json.dumps(
            sub_name), headers={
                "content-type": "application/json",
                "Authorization": "Bearer {}".format(access_token)}
        )
    assert response.status_code == resp_code
    assert msg in response.data


@pytest.mark.parametrize("sub_id, resp_code", get_sub_categories_data)
def test_get_specific_subcategory(test_client, sub_id, resp_code):
    access_token = get_admin_token(test_client)
    response = test_client.get(
        "api/v2/subcategories/" + str(sub_id), headers={
            "Authorization": "Bearer {}".format(access_token)})
    assert response.status_code == resp_code


@pytest.mark.parametrize("sub_name, resp_code, sub_id, msg", update_sub_categories_data)
def test_update_subcategories(test_client, sub_name, resp_code, sub_id, msg):
    access_token = get_admin_token(test_client)
    response = test_client.put(
        "api/v2/subcategories/" + str(sub_id), data=json.dumps(
            sub_name), headers={
                "content-type": "application/json",
                "Authorization": "Bearer {}".format(access_token)}
        )
    assert response.status_code == resp_code
    assert msg in response.data