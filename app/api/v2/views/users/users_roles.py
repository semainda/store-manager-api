"""Module that defines user_roles endpoints"""
# thirdparty imports
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

# local imports
from app.api.v2.models.users.users import UserModel
from app.api.v2.models.users.roles import RoleModel
from app.api.v2.models.users.user_roles import UserRoleModel
from app.api.v2.responses.models.base import ModelResponses
from app.api.v2.responses.auth.base import AuthResponses
from app.api.v2.responses.validators.base import ValidatorsResponse
from app.api.v2.utils.validators import input_validators


class Initializer:
    """Method that initializes required classes"""
    def __init__(self):
        self.resp = AuthResponses()
        self.role = RoleModel()
        self.user = UserModel()
        self.user_role = UserRoleModel()
        self.modresp = ModelResponses()
        self.validator = ValidatorsResponse()
        self.response = ""


class UserRoles(Resource, Initializer):
    """Class that creates and ruturn user_roles"""    
    @jwt_required
    def get(self):
        """Method that return user_roles"""
        if get_jwt_identity():
            user_ = get_jwt_identity()
            if user_["role_name"] == "store_owner": 
                user_roles = self.user_role.get_user_roles()
                self.response = self.modresp.exist_response(user_roles, "User_roles")
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response

    @jwt_required
    def post(self):
        """Method that admin assign role to a user"""
        if get_jwt_identity():
            user_ = get_jwt_identity()
            if user_["role_name"] == "store_owner":
                PARSER = reqparse.RequestParser()
                PARSER.add_argument(
                    "user_id", required=True, type=int, help="Key user_id not found")
                PARSER.add_argument(
                    "role_id", required=True, type=int, help="Key role_id not found")
                data_parsed = PARSER.parse_args()
                role_id = data_parsed["role_id"]
                user_id = data_parsed["user_id"]
                is_valid = input_validators(role_id=role_id, user_id=user_id)
                if is_valid[0]:
                    # checking if role exists
                    role = self.role.get_role_by_id(role_id)
                    if role:
                        # checkin if user exists
                        user = self.user.get_user_by_user_id(user_id)
                        if user:
                            self.user_role.create_user_roles(
                                role_id, user_id)
                            self.response = self.modresp.create_response("User_role")
                        else:
                            self.response = self.modresp.does_not_exist_response(user_id, "User")
                    else:
                        self.response = self.modresp.does_not_exist_response(role_id, "Role")
                else:
                    self.response = self.validator.invalid_contents_response(
                        is_valid[1])
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response


class UserRolesActivity(Resource, Initializer):
    """Class that handels endpoints that requires unique ids"""
    @jwt_required
    def get(self, role_id):
        """Method that return a specific role"""
        if get_jwt_identity():
            user_ = get_jwt_identity()
            if user_["role_name"] == "store_owner": 
                user_id = self.user_role.get_user_role(role_id)
                if user_id:
                    self.response = self.modresp.exist_response(user_id, "Users")
                else:
                    self.response = self.modresp.does_not_exist_response(user_id, "User")
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response

class UpdateUserRole(Resource, Initializer):
    @jwt_required
    def put(self, user_id):
        """Method that return a specific role"""
        if get_jwt_identity():
            user_ = get_jwt_identity()
            if user_["role_name"] == "store_owner":
                PARSER = reqparse.RequestParser()
                PARSER.add_argument(
                    "role_id", required=True, type=int, help="Key role_id not found")
                data_parsed = PARSER.parse_args()
                role_id = data_parsed["role_id"]
                is_valid = input_validators(role_id=role_id)
                if is_valid[0]:
                    role_id = self.user_role.get_user_role_by_id(user_id)
                    if role_id:
                        self.user_role.update_user_roles(
                            user_id, role_id)
                    else:
                        self.response = self.modresp.does_not_exist_response(user_id, "User")
                else:
                    self.response = self.validator.invalid_contents_response(
                        is_valid[1])
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response
