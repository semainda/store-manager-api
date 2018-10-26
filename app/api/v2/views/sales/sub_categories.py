"""Module that defines categories endpoints"""
# thirdparty imports
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

# local imports
from app.api.v2.models.sales.categories import CategoriesModel
from app.api.v2.models.sales.sub_categories import SubCategoriesModel
from app.api.v2.responses.models.base import ModelResponses
from app.api.v2.responses.auth.base import AuthResponses
from app.api.v2.responses.validators.base import ValidatorsResponse
from app.api.v2.utils.validators import input_validators

PARSER = reqparse.RequestParser()
PARSER.add_argument(
    "sub_cat_name",
    required=True, type=str, help="Key sub_cat_name not found")
PARSER.add_argument(
    "cat_id", required=True, type=int, help="Key cat_id not found")
     

class Initializer:
    """Method that initializes required classes"""
    def __init__(self):
        self.resp = AuthResponses()
        self.cat = CategoriesModel()
        self.sub = SubCategoriesModel()
        self.modresp = ModelResponses()
        self.validator = ValidatorsResponse()
        self.response = ""


class SubCategories(Resource, Initializer):
    """Class that creates and ruturn categories"""
    @jwt_required
    def get(self):
        """Method that return categories"""
        if get_jwt_identity():
            user_ = get_jwt_identity()
            if user_["role_name"] == "store_owner":
                subcategories = self.sub.get_all_sub_categories()
                if subcategories:
                    self.response = self.modresp.exists_response(subcategories, "SubCategories")
                else:
                    self.response = self.modresp.does_not_exists_response("SubCategories")
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response

    @jwt_required
    def post(self):
        """Method that creates sub_categories"""
        if get_jwt_identity():
            user_ = get_jwt_identity()
            if user_["role_name"] == "store_owner":
                data_parsed = PARSER.parse_args()
                sub_cat_name = data_parsed["sub_cat_name"].lower()
                cat_id = data_parsed["cat_id"]
                is_valid = input_validators(
                    cat_id=cat_id, sub_cat_name=sub_cat_name)
                if is_valid[0]:
                    category = self.cat.get_category_by_id(cat_id)
                    if category:
                        subcategory = self.sub.get_sub_category_by_id(cat_id)
                        if not subcategory:
                            self.sub.create_sub_categories(sub_cat_name, cat_id)
                            self.response = self.modresp.create_response("SubCategory")
                        else:
                            self.response = self.modresp.already_exist_response("SubCategory")
                    else:
                        self.response = self.modresp.does_not_exist_response(cat_id, "SubCategory")
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
    def get(self, cat_id):
        """Method that returns a sub_category by cat_id"""
        if get_jwt_identity():
            user_ = get_jwt_identity()
            if user_["role_name"] == "store_owner":
                subcategory = self.sub.get_sub_category_by_id(cat_id)
                if subcategory:
                    self.response = self.modresp.exist_response(subcategory, "SubCategory")
                else:
                    self.response = self.modresp.does_not_exist_response(cat_id, "SubCategory")
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response

    @jwt_required
    def put(self, cat_id):
        """Method that returns a sub_category by cat_id"""
        if get_jwt_identity():
            user_ = get_jwt_identity()
            if user_["role_name"] == "store_owner":
                data_parsed = PARSER.parse_args()
                sub_cat_name = data_parsed["sub_cat_name"].lower()
                cat_id = data_parsed["cat_id"]
                is_valid = input_validators(
                    cat_id=cat_id, sub_cat_name=sub_cat_name)
                if is_valid[0]:
                    subcategory = self.sub.get_sub_category_by_id(cat_id)
                    if subcategory:
                        self.sub.update_sub_categories(sub_cat_name, cat_id)
                        self.response = self.modresp.update_response(cat_id, "SubCategory")
                    else:
                        self.response = self.modresp.does_not_exist_response(cat_id, "SubCategory")
                else:
                    self.response = self.validator.invalid_contents_response(
                        is_valid[1])
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response
  