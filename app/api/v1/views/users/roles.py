"""Module that defines roles endpoints"""
# thirdparty imports
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

# local imports
from app.api.v1.auth.user_auth import UserAuth
from app.api.v1.models.users.roles import RoleModel
from app.api.v1.models.users.user_roles import UserRoleModel
from app.api.v1.responses.auth.base import AuthResponses
from app.api.v1.responses.validators.base import ValidatorsResponse
from app.api.v1.utils.validators import input_validators


PARSER = reqparse.RequestParser()
PARSER.add_argument(
    "role_name", required=True, type=str, help="Key role_name not found")


class Initializer:
    """Method that initializes required classes"""
    def __init__(self):
        self.auth = UserAuth()
        self.resp = AuthResponses()
        self.role = RoleModel()
        self.user_role = UserRoleModel()
        self.validator = ValidatorsResponse()
        self.response = ""


class Roles(Resource, Initializer):
    """Class that creates and ruturn roles"""
    def __init__(self):
        super().__init__()
    
    @jwt_required
    def get(self):
        """Method that return roles"""
        if get_jwt_identity():
            user_role_name = self.auth.return_role_name(get_jwt_identity())
            if user_role_name == "store_owner":
                self.response = self.role.get_roles()
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response

    @jwt_required
    def post(self):
        """Method that creates roles"""
        if get_jwt_identity():
            user_role_name = self.auth.return_role_name(get_jwt_identity())
            if user_role_name == "store_owner":
                data_parsed = PARSER.parse_args()
                role_name = data_parsed["role_name"]
                is_valid = input_validators(role_name=role_name)
                if is_valid[0]:
                    self.response = self.role.create_roles(role_name)
                else:
                    self.response = self.validator.invalid_contents_response(
                        is_valid[1])
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response


class RolesActivity(Resource, Initializer):
    """Class that handels endpoints that requires unique ids"""
    @jwt_required
    def get(self, role_id):
        """Method that return a specific role"""
        if get_jwt_identity():
            user_role_name = self.auth.return_role_name(get_jwt_identity())
            if user_role_name == "store_owner":
                self.response = self.role.get_role(role_id)
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response

    @jwt_required
    def delete(self, role_id):
        """Method that return a specific role"""
        if get_jwt_identity():
            user_role_name = self.auth.return_role_name(get_jwt_identity())
            if user_role_name == "store_owner":
                role = self.role.get_entry_by_any_field("id", role_id)
                if role:
                    user_role = self.user_role.get_entry_by_any_field(
                        "role_id", role_id)
                    if user_role:
                        self.response = {
                            "Message": 
                            "This role has already being assigned to users."
                            "To delete it, revoke it from users"}, 400
                    else:
                        self.response = self.role.delete_roles(role_id)
                else:
                    self.response = self.role.get_role(role_id)
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response
    
    @jwt_required
    def put(self, role_id):
        """Method that return a specific role"""
        if get_jwt_identity():
            user_role_name = self.auth.return_role_name(get_jwt_identity())
            if user_role_name == "store_owner":
                data_parsed = PARSER.parse_args()
                role_name = data_parsed["role_name"]
                is_valid = input_validators(role_name=role_name)
                if is_valid[0]:
                    role = self.role.get_entry_by_any_field("id", role_id)
                    if role:
                        self.response = self.role.update_roles(role_id, role_name)
                    else:
                        self.response = self.role.get_role(role_id)
                else:
                    self.response = self.validator.invalid_contents_response(
                        is_valid[1])
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response
