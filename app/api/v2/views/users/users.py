"""Module that defines users endpoints"""
from datetime import datetime

# thirdparty imports
from flask_restful import current_app, Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from passlib.hash import pbkdf2_sha256 as hash256

# local imports
from app.api.v2.auth.user_auth import UserAuth
from app.api.v2.models.users.users import UserModel
from app.api.v2.responses.models.base import ModelResponses
from app.api.v2.utils.validators import input_validators

PARSER = reqparse.RequestParser()
PARSER.add_argument(
    "first_name", required=True, type=str,
    help="Key first_name is not found or value given is not of required type."
        "Make sure a value is 'string' type")
PARSER.add_argument(
    "last_name", required=True, type=str,
    help="Key last_name is not found or value given is not of required type."
        "Make sure a value is 'string' type")
PARSER.add_argument(
    "email", required=True, type=str,
    help="Key email is not found or value given is not of required type."
        "Make sure a value is 'string' type")
PARSER.add_argument(
    "user_name", required=True, type=str,
    help="Key user_name is not found or value given is not of required type."
        "Make sure a value is 'string' type")


class Initializer:
    """Method that initializes required classes"""
    @jwt_required
    def __init__(self):
        self.auth = UserAuth()
        self.user = UserModel()
        self.resp = ModelResponses()
        self.super_user = current_app.config["DEFAULT_ADMIN"]["role_name"]
        self.loggein_user = get_jwt_identity()["role_name"]
        self.response = ""


class Users(Resource, Initializer):
    """Class that creates and ruturn users"""
    def get(self):
        """Method that  gets resources"""
        if get_jwt_identity():
            if  self.loggein_user == self.super_user:       
                users = self.user.get_users()
                if users:
                    self.response = self.resp.exists_response(users, "Store Users")
                else:
                    self.response = self.resp.does_not_exists_response("Users")
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response 

    def post(self):
        """Method that creates users"""
        if get_jwt_identity():
            if self.loggein_user == self.super_user:
                data_parsed = PARSER.parse_args()
                first_name = data_parsed["first_name"].lower()
                last_name = data_parsed["last_name"].lower()
                email = data_parsed["email"].lower()
                user_name = data_parsed["user_name"].lower()
                password = self.auth.generate_hash_password(last_name)
                is_valid = input_validators(first_name=first_name, last_name=last_name, user_name=user_name)
                if is_valid[0]:
                    current_user_name = self.user.get_user("user_name", user_name)
                    current_user_email = self.user.get_user("email", email)
                    if not current_user_name:
                        if not current_user_email:
                            self.user.create_user(
                                first_name, last_name, email, user_name, password)
                            self.response = self.resp.create_response("User", user_name)
                        else:
                            self.response = self.resp.already_exist_response("User", email)
                    else:
                        self.response = self.resp.already_exist_response("User", user_name)
                else:
                    self.response = self.resp.invalid_contents_response(is_valid[1])
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response


class UsersActivity(Resource, Initializer):
    """Class that handels endpoints that requires unique ids"""
    def get(self, user_id):
        """Method that return a specific role"""
        if get_jwt_identity():
            if self.loggein_user == self.super_user:
                user = self.user.get_user("user_id", user_id)
                if user:
                    self.response = self.resp.exist_response(user, "Store User")
                else:
                    self.response = self.resp.does_not_exist_response("user_id", user_id, "User")
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response


class UserProfile(Resource, Initializer):
    """Method that returns ones profile details"""
    def get(self):
        """Method that return a profile"""
        if get_jwt_identity():
            user_ = get_jwt_identity()
            if user_:
                self.response = self.user.get_user("user_id", user_["user_id"])
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response
