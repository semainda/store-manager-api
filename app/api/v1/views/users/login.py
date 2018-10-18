"""Module that handle user logins"""
# thirdparty imports
from flask_restful import Resource, reqparse
# local imports
from ...auth.user_auth import UserAuth
from ...models.users.users import UserModel
from ...responses.auth.base import AuthResponses

PARSER = reqparse.RequestParser()
PARSER.add_argument(
    "user_name", required=True, type=str, help="Key user_name not found")
PARSER.add_argument(
    "password", required=True, type=str, help="Key password not found")


class Login(Resource):
    """Class that perfom login checks"""
    def __init__(self):
        self.auth = UserAuth()
        self.resp = AuthResponses()
        self.user = UserModel()
        self.response = ""

    def post(self):
        """Method that create user login"""
        data_parsed = PARSER.parse_args()
        user_data = self.user.get_user_by_field(
            "user_name", data_parsed["user_name"])
        if user_data:
            if self.auth.verify_hashed_password(
                    data_parsed["password"], user_data[0]["password"]):
                access_token = self.auth.return_access_token(
                    user_data[0]["user_id"])
                self.response = self.resp.user_success_login_response(
                    user_data[0]["user_name"], access_token)
            else:
                self.response = self.resp.user_login_with_error_response()
        else:
            self.response = self.resp.user_login_with_error_response()
        return self.response
