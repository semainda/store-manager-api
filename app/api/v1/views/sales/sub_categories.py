"""Module that defines categories endpoints"""
# thirdparty imports
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

# local imports
from app.api.v1.auth.user_auth import UserAuth
from app.api.v1.models.sales.categories import CategoriesModel
from app.api.v1.models.sales.sub_categories import SubCategoriesModel
from app.api.v1.responses.auth.base import AuthResponses
from app.api.v1.responses.validators.base import ValidatorsResponse
from app.api.v1.utils.validators import input_validators

PARSER = reqparse.RequestParser()
PARSER.add_argument(
    "sub_cat_name",
    required=True, type=str, help="Key sub_cat_name not found")
PARSER.add_argument(
    "cat_id", required=True, type=int, help="Key cat_id not found")
     

class Initializer:
    """Method that initializes required classes"""
    def __init__(self):
        self.auth = UserAuth()
        self.resp = AuthResponses()
        self.cat = CategoriesModel()
        self.sub = SubCategoriesModel()
        self.validator = ValidatorsResponse()
        self.response = ""


class SubCategories(Resource, Initializer):
    """Class that creates and ruturn categories"""
    def __init__(self):
        super().__init__()
    
    @jwt_required
    def get(self):
        """Method that return sub_categories"""
        if get_jwt_identity():
            user_role_name = self.auth.return_role_name(get_jwt_identity())
            if user_role_name == "store_owner":
                self.response = self.sub.get_sub_categories()
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response

    @jwt_required
    def post(self):
        """Method that creates sub_categories"""
        if get_jwt_identity():
            user_role_name = self.auth.return_role_name(get_jwt_identity())
            if user_role_name == "store_owner":
                data_parsed = PARSER.parse_args()
                sub_cat_name = data_parsed["sub_cat_name"].lower()
                cat_id = data_parsed["cat_id"]
                is_valid = input_validators(
                    cat_id=cat_id, sub_cat_name=sub_cat_name)
                if is_valid[0]:
                    category = self.cat.get_entry_by_any_field("id", cat_id)
                    if category:
                        self.response = self.sub.create_sub_categories(
                            sub_cat_name, cat_id)
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


class SubCategoriesActivity(Resource, Initializer):
    """Class that handels endpoints that requires unique ids"""
    @jwt_required
    def get(self, sub_cat_id):
        """Method that returns a sub_category by cat_id"""
        if get_jwt_identity():
            user_role_name = self.auth.return_role_name(get_jwt_identity())
            if user_role_name == "store_owner":
                self.response = self.sub.get_sub_category(sub_cat_id)
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response
    
    @jwt_required
    def put(self, sub_cat_id):
        """Method that returns a sub_category by cat_id"""
        if get_jwt_identity():
            user_role_name = self.auth.return_role_name(get_jwt_identity())
            if user_role_name == "store_owner":
                data_parsed = PARSER.parse_args()
                sub_cat_name = data_parsed["sub_cat_name"].lower()
                cat_id = data_parsed["cat_id"]
                is_valid = input_validators(
                    cat_id=cat_id, sub_cat_name=sub_cat_name)
                if is_valid[0]:
                    sub_category = self.sub.get_entry_by_any_field(
                        "id", sub_cat_id)
                    if sub_category:
                        self.response = self.sub.update_sub_categories(
                            sub_cat_id, sub_cat_name, cat_id)
                    else:
                        self.response = self.sub.get_sub_category(sub_cat_id)
                else:
                    self.response = self.validator.invalid_contents_response(
                        is_valid[1])
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response
  