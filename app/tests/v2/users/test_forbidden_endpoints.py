import json
import pytest
from ..access_token import get_admin_token, get_attendant_token
from ..get_tests_data import atttendant_forbiden_get_endpoints


def test_forbidden_admin_post_endpoints(test_client):
    access_token = get_admin_token(test_client)
    response = test_client.post(
        "api/v2/sales", data=json.dumps(dict(prod_id=1, quantity=10)),
        headers={
            "content-type": "application/json",
            "Authorization": "Bearer {}".format(access_token)})
    assert response.status_code == 403
    assert b"Your not authorized to access this resource. Make sure you have assigned the required role to access this resource" in response.data


@pytest.mark.parametrize("get_endpoint", atttendant_forbiden_get_endpoints)
def test_forbidden_attendant_get_endpoints(test_client, get_endpoint):
    access_token = get_attendant_token(test_client)
    response = test_client.get(
        get_endpoint, headers={
            "Authorization": "Bearer {}".format(access_token)})
    assert response.status_code == 403
    assert b"Your not authorized to access this resource. Make sure you have assigned the required role to access this resource" in response.data