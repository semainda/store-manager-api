"""Module that defines roles endpoints"""
# thirdparty imports
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

# local imports
from app.api.v2.auth.user_auth import UserAuth
from app.api.v2.models.users.roles import RoleModel
# from app.api.v2.models.users.user_roles import UserRoleModel
from app.api.v2.responses.auth.base import AuthResponses
from app.api.v2.responses.models.base import ModelResponses
from app.api.v2.responses.validators.base import ValidatorsResponse
from app.api.v2.utils.validators import input_validators


PARSER = reqparse.RequestParser()
PARSER.add_argument(
    "role_name", required=True, type=str, help="Key role_name not found")


class Initializer:
    """Method that initializes required classes"""
    def __init__(self):
        self.auth = UserAuth()
        self.resp = AuthResponses()
        self.role = RoleModel()
        # self.user_role = UserRoleModel()
        self.modresp = ModelResponses()
        self.validator = ValidatorsResponse()
        self.response = ""


class Roles(Resource, Initializer):
    """Class that creates and ruturn roles"""
    @jwt_required
    def post(self):
        """Method that creates roles"""
        if get_jwt_identity():
            user_ = get_jwt_identity()
            if user_["role_name"] == "store_owner":
                data_parsed = PARSER.parse_args()
                role_name = data_parsed["role_name"]
                is_valid = input_validators(role_name=role_name)
                if is_valid[0]:
                    role = self.role.get_role_by_name(role_name)
                    if not role:
                        self.role.create_role(role_name)
                        self.response = self.modresp.create_response("Role")
                    else:
                        self.response = self.modresp.already_exist_response("Role")
                else:
                    self.response = self.validator.invalid_contents_response(
                        is_valid[1])
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response
