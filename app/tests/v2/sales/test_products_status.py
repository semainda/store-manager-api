"""Module that tests products_status endpoints"""
import json
import pytest
from ..get_tests_data import get_products_status_data
from .. access_token import get_admin_token


@pytest.mark.run(order=11)
def test_get_products_status(test_client):
    access_token = get_admin_token(test_client)
    response = test_client.get(
        "api/v2/products/status", headers={
            "Authorization": "Bearer {}".format(access_token)})
    assert response.status_code == 200


@pytest.mark.parametrize("p_id, resp_code", get_products_status_data)
def test_get_specific_product_status(test_client, p_id, resp_code):
    access_token = get_admin_token(test_client)
    response = test_client.get(
        "api/v2/products/status/" + str(p_id), headers={
            "Authorization": "Bearer {}".format(access_token)})
    assert response.status_code == resp_code