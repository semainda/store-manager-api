"""Module that defines users endpoints"""
from datetime import datetime

# thirdparty imports
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from passlib.hash import pbkdf2_sha256 as hash256

# local imports
from app.api.v1.auth.user_auth import UserAuth
from app.api.v1.models.users.users import UserModel
from app.api.v1.responses.auth.base import AuthResponses
from app.api.v1.responses.validators.base import ValidatorsResponse
from app.api.v1.utils.validators import input_validators

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
        self.validator = ValidatorsResponse()
        self.response = ""


class Users(Resource, Initializer):
    """Class that creates and ruturn users"""
    @jwt_required
    def get(self):
        """Method that get users"""
        if get_jwt_identity():
            user_id = get_jwt_identity()
            user_role_name = self.auth.return_role_name(user_id)
            if user_role_name == "store_owner":
                self.response = self.user.get_users()
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response       

    @jwt_required
    def post(self):
        """Method that creates users"""
        if get_jwt_identity():
            user_id = get_jwt_identity()
            user_role_name = self.auth.return_role_name(user_id)
            if user_role_name == "store_owner":
                data_parsed = PARSER.parse_args()
                first_name = data_parsed["first_name"].lower()
                last_name = data_parsed["last_name"].lower()
                email = data_parsed["email"].lower()
                user_name = data_parsed["user_name"].lower()
                password = hash256.hash(last_name)
                created_at = datetime.now().strftime("%c")
                is_valid = input_validators(
                    first_name=first_name, last_name=last_name,
                    user_name=user_name)
                if is_valid[0]:
                    self.response = self.user.create_users(
                        first_name, last_name, email,
                        user_name, password, created_at)
                else:
                    self.response = self.validator.invalid_contents_response(
                        is_valid[1])
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
            user_role_name = self.auth.return_role_name(get_jwt_identity())
            if user_role_name == "store_owner":
                self.response = self.user.get_user(user_id)
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response

    @jwt_required
    def put(self):
        """Method that return a specific role"""
        if get_jwt_identity():
            user_id = get_jwt_identity()
            if user_id:
                PARSER.add_argument(
                    "password", required=True, type=str, help="Key password not found")
                data_parsed = PARSER.parse_args()
                first_name = data_parsed["first_name"].lower()
                last_name = data_parsed["last_name"].lower()
                email = data_parsed["email"].lower()
                user_name = data_parsed["user_name"].lower()
                password = hash256.hash(data_parsed["password"])
                is_valid = input_validators(
                    first_name=first_name, last_name=last_name,
                    user_name=user_name)
                if is_valid[0]:
                    self.response = self.user.update_users(
                        user_id, first_name, last_name, email, user_name, password)
                else:
                    self.response = self.validator.invalid_contents_response(
                        is_valid[1])
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response


class UserProfile(Resource, Initializer):
    """Method that returns ones profile details"""
    @jwt_required
    def get(self):
        """Method that return a profile"""
        if get_jwt_identity():
            user_id = get_jwt_identity()
            if user_id:
                self.response = self.user.get_user(user_id)
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response