"""Module that returns store admin/attendant login access token"""
import json

def get_admin_token(client):
    """Function that return store admin login access token"""
    admin_data = dict(
            user_name="semainda",
            password="mk911212"
        )
    response = client.post(
        "api/v2/auth/login", data=json.dumps(admin_data),
        headers={"content-type": "application/json"})
    return json.loads(response.data.decode())["Token"]


def get_attendant_token(client):
    """Function that return store attendant login access token"""
    attendant_data = dict(
            user_name="said",
            password="semainda"
        )
    response = client.post(
        "api/v2/auth/login", data=json.dumps(attendant_data),
        headers={"content-type": "application/json"})
    return json.loads(response.data.decode())["Token"]