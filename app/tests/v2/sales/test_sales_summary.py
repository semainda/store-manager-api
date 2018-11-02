"""Module that tests sales summary endpoints"""
import json
import pytest
from ..get_tests_data import get_sales_summary_by_user_id_data
from .. access_token import get_admin_token, get_attendant_token


@pytest.mark.run(order=13)
def test_admin_get_store_sales_summary_(test_client):
    access_token = get_admin_token(test_client)
    response = test_client.get(
        "api/v2/sales/store/summary", headers={
            "Authorization": "Bearer {}".format(access_token)})
    assert response.status_code == 404


@pytest.mark.run(order=13)
def test_admin_get_all_attendants_sales_summary_(test_client):
    access_token = get_admin_token(test_client)
    response = test_client.get(
        "api/v2/sales/summary", headers={
            "Authorization": "Bearer {}".format(access_token)})
    assert response.status_code == 404


@pytest.mark.run(order=13)
def test_attendant_get_all_own_sales_summary_(test_client):
    access_token = get_attendant_token(test_client)
    response = test_client.get(
        "api/v2/sales/mysales", headers={
            "Authorization": "Bearer {}".format(access_token)})
    assert response.status_code == 404


def test_admin_get_store_sales_summary(test_client):
    access_token = get_admin_token(test_client)
    response = test_client.get(
        "api/v2/sales/store/summary", headers={
            "Authorization": "Bearer {}".format(access_token)})
    assert response.status_code == 200


def test_admin_get_all_attendants_sales_summary(test_client):
    access_token = get_admin_token(test_client)
    response = test_client.get(
        "api/v2/sales/summary", headers={
            "Authorization": "Bearer {}".format(access_token)})
    assert response.status_code == 200


@pytest.mark.parametrize("user_id, resp_code", get_sales_summary_by_user_id_data)
def test_admin_attendant_sales_summary_id(test_client, user_id, resp_code):
    access_token = get_admin_token(test_client)
    response = test_client.get(
        "api/v2/sales/summary/" + str(user_id),
        headers={
            "Authorization": "Bearer {}".format(access_token)})
    assert response.status_code == resp_code


def test_attendant_get_all_own_sales_summary(test_client):
    access_token = get_attendant_token(test_client)
    response = test_client.get(
        "api/v2/sales/mysales", headers={
            "Authorization": "Bearer {}".format(access_token)})
    assert response.status_code == 200
