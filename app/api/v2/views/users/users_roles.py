"""Module that defines user_roles endpoints"""
# thirdparty imports
from flask_restful import current_app, Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

# local imports
from app.api.v2.models.users.users import UserModel
from app.api.v2.models.users.roles import RoleModel
from app.api.v2.models.users.user_roles import UserRoleModel
from app.api.v2.responses.models.base import ModelResponses
from app.api.v2.utils.validators import input_validators


class Initializer:
    """Method that initializes required classes"""
    @jwt_required
    def __init__(self):
        self.role = RoleModel()
        self.user = UserModel()
        self.user_role = UserRoleModel()
        self.resp = ModelResponses()
        self.super_user = current_app.config["DEFAULT_ADMIN"]["role_name"]
        self.loggein_user = get_jwt_identity()["role_name"]
        self.response = ""


class UserRoles(Resource, Initializer):
    """Class that creates and ruturn user_roles"""    
    def get(self):
        """Method that return user_roles"""
        if get_jwt_identity():
            if self.loggein_user == self.super_user: 
                user_roles = self.user_role.get_user_roles()
                self.response = self.resp.exist_response(user_roles, "User_roles")
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response

    def post(self):
        """Method that admin assign role to a user"""
        if get_jwt_identity():
            if self.loggein_user == self.super_user:
                PARSER = reqparse.RequestParser()
                PARSER.add_argument(
                    "user_id", required=True, type=int,
                    help="Key user_id is not found or value given is not of required type."
                        "Make sure a value is 'integer' type")
                PARSER.add_argument(
                    "role_id", required=True, type=int,
                    help="Key role_id is not found or value given is not of required type."
                        "Make sure a value is 'integer' type")
                data_parsed = PARSER.parse_args()
                role_id = data_parsed["role_id"]
                user_id = data_parsed["user_id"]
                is_valid = input_validators(role_id=role_id, user_id=user_id)
                if is_valid[0]:
                    # checking if role exists
                    role = self.role.get_role("role_id", role_id)
                    if role:
                        # checkin if user exists
                        user = self.user.get_user("user_id", user_id)
                        if user:
                            try:
                                self.user_role.create_user_roles(
                                    role_id, user_id)
                            except:
                                return self.resp.already_exist_response("User_role", (role_id, user_id))
                            self.response = self.resp.create_response("User_role", (role_id, user_id))
                        else:
                            self.response = self.resp.does_not_exist_response("user_id", user_id, "User")
                    else:
                        self.response = self.resp.does_not_exist_response("role_id", role_id, "Role")
                else:
                    self.response = self.resp.invalid_contents_response(
                        is_valid[1])
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response


class UserRolesActivity(Resource, Initializer):
    """Class that handels endpoints that requires unique ids"""
    def get(self, role_id):
        """Method that return a all users with given role_id"""
        if get_jwt_identity():
            if self.loggein_user == self.super_user: 
                user_roles = self.user_role.get_user_role("role_id", role_id)
                if user_roles:
                    self.response = self.resp.exist_response(user_roles, "Users")
                else:
                    self.response = self.resp.does_not_exist_response("role_id", role_id, "Users")
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response

    def put(self, role_id):
        """Method that update all users role with given role_id """
        if get_jwt_identity():
            if self.loggein_user == self.super_user:
                PARSER = reqparse.RequestParser()
                PARSER.add_argument(
                    "role_id", required=True, type=int,
                    help="Key role_id is not found or value given is not of required type."
                        "Make sure a value is 'integer' type")
                data_parsed = PARSER.parse_args()
                new_role_id = data_parsed["role_id"]
                is_valid = input_validators(role_id=role_id)
                if is_valid[0]:
                    user_role_id = self.user_role.get_user_role("role_id", role_id)
                    if user_role_id:
                        new_role = self.role.get_role("role_id", new_role_id)
                        if new_role:
                            updated_list = [
                                self.user_role.update_user_roles(
                                    user["user_id"], new_role_id)
                                    for user in user_role_id if user["user_id"] != get_jwt_identity()["user_id"]]
                            if updated_list:
                                self.response = self.resp.update_response("role_id for ", updated_list[0], "User_role")
                            else:
                                self.response = self.resp.forbidden_super_user_role_update_response(self.super_user)
                        else:
                            self.response = self.resp.does_not_exist_response("role_id", new_role_id, "User_role")
                    else:
                        self.response = self.resp.does_not_exist_response("role_id", role_id, "User_role")
                else:
                    self.response = self.resp.invalid_contents_response(
                        is_valid[1])
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response


class UserRoleActivity(Resource, Initializer):
    """Method that handels specific user role given user_role_id"""
    def get(self, user_role_id):
        """Method that return a all users with fiven role_id"""
        if get_jwt_identity():
            if self.loggein_user == self.super_user: 
                user_role = self.user_role.get_user_role("user_role_id", user_role_id)
                if user_role:
                    self.response = self.resp.exist_response(user_role, "User_role")
                else:
                    self.response = self.resp.does_not_exist_response("user_role_id", user_role_id, "User_role")
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response

    def put(self, user_role_id):
        """Method that return a specific role"""
        if get_jwt_identity():
            if self.loggein_user == self.super_user:
                PARSER = reqparse.RequestParser()
                PARSER.add_argument(
                    "role_id", required=True, type=int,
                    help="Key role_id is not found or value given is not of required type."
                        "Make sure a value is 'integer' type")
                data_parsed = PARSER.parse_args()
                role_id = data_parsed["role_id"]
                is_valid = input_validators(role_id=role_id)
                if is_valid[0]:
                    user_role= self.user_role.get_user_role("user_role_id", user_role_id)
                    if user_role:
                        user_role = user_role[0]
                        if user_role["user_id"] != get_jwt_identity()["user_id"]:
                            self.user_role.update_user_roles(
                                user_role["user_id"], role_id)
                            self.response = self.resp.update_response("user_role_id", user_role_id, "User_role")
                        else:
                            self.response = self.resp.forbidden_super_user_role_update_response(self.super_user)   
                    else:
                        self.response = self.resp.does_not_exist_response("user_role_id", user_role_id, "User_role")
                else:
                    self.response = self.resp.invalid_contents_response(
                        is_valid[1])
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response
