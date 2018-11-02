"""Module that tests sales endpoints"""
import json
import pytest
from ..get_tests_data import create_sale_data, get_sales_by_user_id_data,\
get_attendant_own_sales_by_sale_id_data
from .. access_token import get_admin_token, get_attendant_token


@pytest.mark.run(order=12)
def test_admin_get_sales_(test_client):
    access_token = get_admin_token(test_client)
    response = test_client.get(
        "api/v2/sales", headers={
            "Authorization": "Bearer {}".format(access_token)})
    assert response.status_code == 404


@pytest.mark.run(order=14)
def test_get_attendant_own_sales(test_client):
    access_token = get_attendant_token(test_client)
    response = test_client.get(
        "api/v2/user/sales", headers={
            "Authorization": "Bearer {}".format(access_token)})
    assert response.status_code == 404


@pytest.mark.run(order=15)
@pytest.mark.parametrize("sel_item, resp_code, msg", create_sale_data)
def test_attendant_create_sales(test_client, sel_item, resp_code, msg):
    access_token = get_attendant_token(test_client)
    response = test_client.post(
        "api/v2/sales", data=json.dumps(
            sel_item), headers={
                "content-type": "application/json",
                "Authorization": "Bearer {}".format(access_token)}
        )
    assert response.status_code == resp_code
    assert msg in response.data


def test_admin_get_sales(test_client):
    access_token = get_admin_token(test_client)
    response = test_client.get(
        "api/v2/sales", headers={
            "Authorization": "Bearer {}".format(access_token)})
    assert response.status_code == 200


@pytest.mark.parametrize("user_id, resp_code", get_sales_by_user_id_data)
def test_admin_get_sales_by_user_id(test_client, user_id, resp_code):
    access_token = get_admin_token(test_client)
    response = test_client.get(
        "api/v2/sales/" + str(user_id), headers={
            "Authorization": "Bearer {}".format(access_token)})
    assert response.status_code == resp_code


def test_get_attendant_own_sales_(test_client):
    access_token = get_attendant_token(test_client)
    response = test_client.get(
        "api/v2/user/sales", headers={
            "Authorization": "Bearer {}".format(access_token)})
    assert response.status_code == 200


@pytest.mark.parametrize(
        "sale_id, resp_code", get_attendant_own_sales_by_sale_id_data)
def test_attendant_get_sales_by_sale_id(test_client, sale_id, resp_code):
    access_token = get_attendant_token(test_client)
    response = test_client.get(
        "api/v2/user/sales/" + str(sale_id), headers={
            "Authorization": "Bearer {}".format(access_token)})
    assert response.status_code == resp_code
