"""Module that defines categories endpoints"""
# thirdparty imports
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

# local imports
from app.api.v2.models.sales.categories import CategoriesModel
from app.api.v2.responses.auth.base import AuthResponses
from app.api.v2.responses.models.base import ModelResponses
from app.api.v2.responses.validators.base import ValidatorsResponse
from app.api.v2.utils.validators import input_validators


PARSER = reqparse.RequestParser()
PARSER.add_argument(
    "cat_name", required=True, type=str, help="Key cat_name not found")
     

class Initializer:
    """Method that initializes required classes"""
    def __init__(self):
        self.resp = AuthResponses()
        self.cat = CategoriesModel()
        self.modresp = ModelResponses()
        self.validator = ValidatorsResponse()
        self.response = ""


class Categories(Resource, Initializer):
    """Class that creates and ruturn categories"""
    @jwt_required
    def get(self):
        """Method that return categories"""
        if get_jwt_identity():
            user_ = get_jwt_identity()
            if user_["role_name"] == "store_owner":
                categories = self.cat.get_all_categories()
                if categories:
                    self.response = self.modresp.exists_response(categories, "Categories")
                else:
                    self.response = self.modresp.does_not_exists_response("Categories")
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response

    @jwt_required
    def post(self):
        """Method that creates categories"""
        if get_jwt_identity():
            user_ = get_jwt_identity()
            if user_["role_name"] == "store_owner":
                data_parsed = PARSER.parse_args()
                cat_name = data_parsed["cat_name"].lower()
                is_valid = input_validators(
                    cat_name=cat_name)
                if is_valid[0]:
                    category = self.cat.get_category_by_name(cat_name)
                    if not category:
                        self.cat.create_category(cat_name)
                        self.response = self.modresp.create_response("Category")
                    else:
                        self.response = self.modresp.already_exist_response("Category")
                else:
                    self.response = self.validator.invalid_contents_response(
                        is_valid[1])
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
            user_ = get_jwt_identity()
            if user_["role_name"] == "store_owner":
                category = self.cat.get_category_by_id(cat_id)
                if category:
                    self.response = self.modresp.exist_response(category, "category")
                else:
                    self.response = self.modresp.does_not_exist_response(cat_id, "Category")
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response
    

    @jwt_required
    def put(self, cat_id):
        """Method that returns a category by cat_id"""
        if get_jwt_identity():
            user_= get_jwt_identity()
            if user_["role_name"] == "store_owner":
                data_parsed = PARSER.parse_args()
                cat_name = data_parsed["cat_name"].lower()
                is_valid = input_validators(cat_name=cat_name)
                if is_valid[0]:
                    category = self.cat.get_category_by_id(cat_id)
                    if category:
                        self.cat.update_category(cat_name, cat_id)
                        self.response = self.modresp.update_response(cat_id, "Category")
                    else:
                        self.response = self.modresp.does_not_exist_response(cat_id, "Category")
                else:
                    self.response = self.validator.invalid_contents_response(
                        is_valid[1])
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response