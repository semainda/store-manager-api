"""Module that defines categories endpoints"""
# thirdparty imports
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

# local imports
from app.api.v1.auth.user_auth import UserAuth
from app.api.v1.models.sales.categories import CategoriesModel
from app.api.v1.responses.auth.base import AuthResponses
from app.api.v1.responses.validators.base import ValidatorsResponse
from app.api.v1.utils.validators import input_validators


PARSER = reqparse.RequestParser()
PARSER.add_argument(
    "cat_name", required=True, type=str, help="Key cat_name not found")
     

class Initializer:
    """Method that initializes required classes"""
    def __init__(self):
        self.auth = UserAuth()
        self.resp = AuthResponses()
        self.cat = CategoriesModel()
        self.validator = ValidatorsResponse()
        self.response = ""


class Categories(Resource, Initializer):
    """Class that creates and ruturn categories"""
    def __init__(self):
        super().__init__()
    
    @jwt_required
    def get(self):
        """Method that return categories"""
        if get_jwt_identity():
            user_role_name = self.auth.return_role_name(get_jwt_identity())
            if user_role_name == "store_owner":
                self.response = self.cat.get_categories()
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response

    @jwt_required
    def post(self):
        """Method that creates categories"""
        if get_jwt_identity():
            user_role_name = self.auth.return_role_name(get_jwt_identity())
            if user_role_name == "store_owner":
                data_parsed = PARSER.parse_args()
                cat_name = data_parsed["cat_name"].lower()
                is_valid = input_validators(
                    cat_name=cat_name)
                if is_valid[0]:
                    self.response = self.cat.create_categories(cat_name)
                else:
                    self.response = self.validator.invalid_contents_response(is_valid[1])
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response


class CategoriesActivity(Resource, Initializer):
    """Class that handels endpoints that requires unique ids"""
    @jwt_required
    def get(self, cat_id):
        """Method that returns a category by cat_id"""
        if get_jwt_identity():
            user_role_name = self.auth.return_role_name(get_jwt_identity())
            if user_role_name == "store_owner":
                self.response = self.cat.get_category(cat_id)
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response
    
    @jwt_required
    def put(self, cat_id):
        """Method that returns a category by cat_id"""
        if get_jwt_identity():
            user_role_name = self.auth.return_role_name(get_jwt_identity())
            if user_role_name == "store_owner":
                data_parsed = PARSER.parse_args()
                cat_name = data_parsed["cat_name"]
                is_valid = input_validators(cat_name=cat_name)
                if is_valid[0]:
                    category = self.cat.get_entry_by_any_field("id", cat_id)
                    if category:
                        self.response = self.cat.update_categories(cat_id, cat_name)
                    else:
                        self.response = self.cat.get_category(cat_id)
                else:
                    self.response = self.validator.invalid_contents_response(
                        is_valid[1])
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response
    
