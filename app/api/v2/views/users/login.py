"""Module that handle user logins"""
# thirdparty imports
from flask_restful import Resource, reqparse
# local imports
from ...auth.user_auth import UserAuth
from ...models.users.users import UserModel
from app.api.v2.responses.models.base import ModelResponses

PARSER = reqparse.RequestParser()
PARSER.add_argument(
    "user_name", required=True, type=str, 
    help="Key user_name is not found or value given is not of required type."
        "Make sure a value is 'string' type")
PARSER.add_argument(
    "password", required=True, type=str, 
    help="Key password is not found or value given is not of required type."
        "Make sure a value is 'string' type")


class Login(Resource):
    """Class that perfom login checks"""
    def __init__(self):
        self.auth = UserAuth()
        self.resp = ModelResponses()
        self.user = UserModel()
        self.response = ""

    def post(self):
        """Method that create user login"""
        data_parsed = PARSER.parse_args()
        user_data = self.user.get_user_login_credentials(data_parsed["user_name"])
        if user_data:
            if self.auth.verify_hashed_password(
                    data_parsed["password"], user_data["password"]):
                access_token = self.auth.return_access_token(
                    {"user_id":user_data["user_id"],
                    "role_name":user_data["role_name"]})
                self.response = self.resp.user_success_login_response(
                    data_parsed["user_name"], access_token)
            else:
                self.response = self.resp.user_login_with_error_response()
        else:
            self.response = self.resp.user_login_with_error_response()
        return self.response
