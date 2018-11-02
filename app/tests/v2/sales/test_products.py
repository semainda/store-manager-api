"""Module that tests products endpoints"""
import json
import pytest
from ..get_tests_data import create_products_data, get_product_data,\
attendant_products_data
from .. access_token import get_admin_token
from .. access_token import get_attendant_token

# Admin tests
@pytest.mark.run(order=8)
def test_admin_get_products(test_client):
    access_token = get_admin_token(test_client)
    response = test_client.get(
        "api/v2/products", headers={
            "Authorization": "Bearer {}".format(access_token)})
    assert response.status_code == 404
    assert b"'Products' are not yet created" in response.data


@pytest.mark.run(order=9)
@pytest.mark.parametrize("product, resp_code, msg", create_products_data)
def test_admin_create_products(test_client, product, resp_code, msg):
    access_token = get_admin_token(test_client)
    response = test_client.post(
        "api/v2/products", data=json.dumps(
            product), headers={
                "content-type": "application/json",
                "Authorization": "Bearer {}".format(access_token)}
        )
    assert response.status_code == resp_code
    assert msg in response.data


@pytest.mark.parametrize("p_id, resp_code", get_product_data)
def test_admin_get_specific_product(test_client, p_id, resp_code):
    access_token = get_admin_token(test_client)
    response = test_client.get(
        "api/v2/products/" + str(p_id), headers={
            "Authorization": "Bearer {}".format(access_token)})
    assert response.status_code == resp_code


# Attendants tests
@pytest.mark.run(order=10)
@pytest.mark.parametrize("product, resp_code, msg", attendant_products_data)
def test_attendant_create_products(test_client, product, resp_code, msg):
    access_token = get_attendant_token(test_client)
    response = test_client.post(
        "api/v2/products", data=json.dumps(
            product), headers={
                "content-type": "application/json",
                "Authorization": "Bearer {}".format(access_token)}
        )
    assert response.status_code == resp_code
    assert msg in response.data


def test_attendant_get_products(test_client):
    access_token = get_attendant_token(test_client)
    response = test_client.get(
        "api/v2/products", headers={
            "Authorization": "Bearer {}".format(access_token)})
    assert response.status_code == 200


@pytest.mark.parametrize("p_id, resp_code", get_product_data)
def test_attendant_get_specific_product(test_client, p_id, resp_code):
    access_token = get_admin_token(test_client)
    response = test_client.get(
        "api/v2/products/" + str(p_id), headers={
            "Authorization": "Bearer {}".format(access_token)})
    assert response.status_code == resp_code

