"""Module that defines users endpoints"""
from datetime import datetime

# thirdparty imports
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from passlib.hash import pbkdf2_sha256 as hash256

# local imports
from app.api.v2.auth.user_auth import UserAuth
from app.api.v2.models.users.users import UserModel
from app.api.v2.responses.auth.base import AuthResponses
from app.api.v2.responses.models.base import ModelResponses
from app.api.v2.responses.validators.base import ValidatorsResponse
from app.api.v2.utils.validators import input_validators

PARSER = reqparse.RequestParser()
PARSER.add_argument(
    "first_name", required=True, type=str, help="Key first_name not found")
PARSER.add_argument(
    "last_name", required=True, type=str, help="Key last_name not found")
PARSER.add_argument(
    "email", required=True, type=str, help="Key email not found")
PARSER.add_argument(
    "user_name", required=True, type=str, help="Key user_name not found")


class Initializer:
    """Method that initializes required classes"""
    def __init__(self):
        self.auth = UserAuth()
        self.resp = AuthResponses()
        self.user = UserModel()
        self.modresp = ModelResponses()
        self.validator = ValidatorsResponse()
        self.response = ""


class Users(Resource, Initializer):
    """Class that creates and ruturn users"""
    @jwt_required
    def get(self):
        """Method that  gets resources"""
        if get_jwt_identity():
            user_ = get_jwt_identity()
            if  user_["role_name"]  == "store_owner":       
                users = self.user.get_all_users()
                if users:
                    self.response = self.modresp.exists_response(users, "Users")
                else:
                    self.response = self.modresp.does_not_exists_response("users")
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response 

    @jwt_required
    def post(self):
        """Method that creates users"""
        if get_jwt_identity():
            user_details = get_jwt_identity()
            if user_details["role_name"] == "store_owner":
                data_parsed = PARSER.parse_args()
                first_name = data_parsed["first_name"].lower()
                last_name = data_parsed["last_name"].lower()
                email = data_parsed["email"]
                user_name = data_parsed["user_name"]
                password = self.auth.generate_hash_password(user_name)
                is_valid = input_validators(first_name=first_name, last_name=last_name)
                if is_valid[0]:
                    current_user = self.user.get_user_by_user_name_email(
                        user_name, email)
                    if not current_user:
                        self.user.create_user(
                            first_name, last_name, email, user_name, password)
                        self.response = self.modresp.create_response("User")
                    else:
                        self.response = self.modresp.already_exist_response("User")
                else:
                    self.response = self.validator.invalid_contents_response(is_valid[1])
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response

class UsersActivity(Resource, Initializer):
    """Class that handels endpoints that requires unique ids"""
    @jwt_required
    def get(self, user_id):
        """Method that return a specific role"""
        if get_jwt_identity():
            user_ = get_jwt_identity()
            if user_["role_name"] == "store_owner":
                user = self.user.get_user_by_user_id(user_id)
                if user:
                    self.response = self.modresp.exist_response(user, "User")
                else:
                    self.response = self.modresp.does_not_exist_response(user_id, "User")
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response
