"""Module that defines roles endpoints"""
# thirdparty imports
from flask_restful import current_app, Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

# local imports
from app.api.v2.models.users.roles import RoleModel
from app.api.v2.models.users.user_roles import UserRoleModel
from app.api.v2.responses.models.base import ModelResponses
from app.api.v2.utils.validators import input_validators


PARSER = reqparse.RequestParser()
PARSER.add_argument(
    "role_name", required=True, type=str, 
    help="Key role_name is not found or value given is not of required type."
        "Make sure a value is 'string' type")


class Initializer:
    """Method that initializes required classes"""
    @jwt_required
    def __init__(self):
        self.role = RoleModel()
        self.user = UserRoleModel()
        self.resp = ModelResponses()
        self.super_user = current_app.config["DEFAULT_ADMIN"][0]
        self.loggein_user = get_jwt_identity()["role_name"]
        self.response = ""


class Roles(Resource, Initializer):
    """Class that creates and ruturn roles"""
    def get(self):
        """Method that return roles"""
        if get_jwt_identity():
            if self.loggein_user == self.super_user:
                roles = self.role.get_roles()
                self.response = self.resp.exists_response(roles, "Store Roles")
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response

    def post(self):
        """Method that creates roles"""
        if get_jwt_identity():
            if self.loggein_user == self.super_user:
                data_parsed = PARSER.parse_args()
                role_name = data_parsed["role_name"]
                is_valid = input_validators(role_name=role_name)
                if is_valid[0]:
                    role = self.role.get_role("role_name", role_name)
                    if not role:
                        self.role.create_role(role_name)
                        self.response = self.resp.create_response("Role", role_name)
                    else:
                        self.response = self.resp.already_exist_response("Role", role_name)
                else:
                    self.response = self.resp.invalid_contents_response(
                        is_valid[1])
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response


class RolesActivity(Resource, Initializer):
    """Class that handels endpoints that requires unique ids"""
    def get(self, role_id):
        """Method that return a specific role"""
        if get_jwt_identity():
            if self.loggein_user == self.super_user:
                role = self.role.get_role("role_id", role_id)
                if role:
                    self.response = self.resp.exist_response(role, "Role")
                else:
                    self.response = self.resp.does_not_exist_response(
                        "role_id", role_id, "Role")
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response

    def put(self, role_id):
        """Method that return a specific role"""
        if get_jwt_identity():
            if self.loggein_user == self.super_user:
                data_parsed = PARSER.parse_args()
                role_name = data_parsed["role_name"].lower()
                is_valid = input_validators(role_name=role_name)
                if is_valid[0]:
                    role = self.role.get_role("role_id", role_id)
                    if role:
                        if role["role_name"] != self.super_user:
                            role_name_ = self.role.get_role("role_name", role_name)
                            if not role_name_:
                                self.role.update_role(role_name, role_id)
                                self.response = self.resp.update_response("role_id", role_id, "Role")
                            else:
                                self.response = self.resp.already_exist_response(
                                    "Role", role_name)
                        else:
                            self.response = self.resp.forbidden_super_user_role_update_response(self.super_user)
                    else:
                       self.response = self.resp.does_not_exist_response(
                           "role_id", role_id, "Role")
                else:
                    self.response = self.resp.invalid_contents_response(
                        is_valid[1])
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response

    def delete(self, role_id):
        """Method that return a specific role"""
        if get_jwt_identity():
            if self.loggein_user == self.super_user:
                role = self.role.get_role("role_id", role_id)
                if role:
                    user_role = self.user.get_user_role("role_id", role_id)
                    if user_role:
                        self.response =\
                        self.resp.forbidden_user_role_delete_response()
                    else:
                        self.role.delete_role("role_id", role_id)
                        self.response = self.resp.delete_response("role_id", role_id, "Role")
                else:
                    self.response = self.resp.does_not_exist_response("role_id", role_id, "Role")
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response
