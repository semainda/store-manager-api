"""Module that defines categories endpoints"""
# thirdparty imports
from flask_restful import current_app, Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

# local imports
from app.api.v2.models.sales.categories import CategoriesModel
from app.api.v2.models.sales.sub_categories import SubCategoriesModel
from app.api.v2.responses.models.base import ModelResponses
from app.api.v2.utils.validators import input_validators

PARSER = reqparse.RequestParser()
PARSER.add_argument(
    "sub_cat_name",
    required=True, type=str,
    help="Key sub_cat_name is not found or value given is not of required type."
        "Make sure a value is 'string' type")
PARSER.add_argument(
    "cat_id", required=True, type=int, 
    help="Key cat_id is not found or value given is not of required type."
        "Make sure a value is 'integer' type")
     

class Initializer:
    """Method that initializes required classes"""
    @jwt_required
    def __init__(self):
        self.resp = ModelResponses()
        self.cat = CategoriesModel()
        self.sub = SubCategoriesModel()
        self.super_user = current_app.config["DEFAULT_ADMIN"][0]
        self.loggein_user = get_jwt_identity()["role_name"]
        self.response = ""


class SubCategories(Resource, Initializer):
    """Class that creates and ruturn categories"""
    def get(self):
        """Method that return categories"""
        if get_jwt_identity():
            if self.loggein_user == self.super_user:
                subcategories = self.sub.get_sub_categories()
                if subcategories:
                    self.response = self.resp.exists_response(subcategories, "SubCategories")
                else:
                    self.response = self.resp.does_not_exists_response("SubCategories")
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response

    def post(self):
        """Method that creates sub_categories"""
        if get_jwt_identity():
            if self.loggein_user == self.super_user:
                data_parsed = PARSER.parse_args()
                sub_cat_name = data_parsed["sub_cat_name"].lower()
                cat_id = data_parsed["cat_id"]
                is_valid = input_validators(
                    cat_id=cat_id, sub_cat_name=sub_cat_name)
                if is_valid[0]:
                    category = self.cat.get_category("cat_id", cat_id)
                    if category:
                        subcategory = self.sub.get_sub_category("sub_name", sub_cat_name)
                        if not subcategory:
                            self.sub.create_sub_categories(sub_cat_name, cat_id)
                            self.response = self.resp.create_response("SubCategory", sub_cat_name)
                        else:
                            self.response = self.resp.already_exist_response("SubCategory", sub_cat_name)
                    else:
                        self.response = self.resp.does_not_exist_response("cat_id", cat_id, "Category")
                else:
                    self.response = self.resp.invalid_contents_response(
                        is_valid[1])
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response


class SubCategoriesActivity(Resource, Initializer):
    """Class that handels endpoints that requires unique ids"""
    def get(self, sub_id):
        """Method that returns a sub_category by cat_id"""
        if get_jwt_identity():
            if self.loggein_user == self.super_user:
                subcategory = self.sub.get_sub_category("sub_id", sub_id)
                if subcategory:
                    self.response = self.resp.exist_response(subcategory, "SubCategory")
                else:
                    self.response = self.resp.does_not_exist_response("sub_id", sub_id, "SubCategory")
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response

    def put(self, sub_id):
        """Method that returns a sub_category by cat_id"""
        if get_jwt_identity():
            if self.loggein_user == self.super_user:
                data_parsed = PARSER.parse_args()
                sub_cat_name = data_parsed["sub_cat_name"].lower()
                cat_id = data_parsed["cat_id"]
                is_valid = input_validators(
                    cat_id=cat_id, sub_cat_name=sub_cat_name)
                if is_valid[0]:
                    subcategory = self.sub.get_sub_category("sub_id", sub_id)
                    if subcategory:
                        category = self.cat.get_category("cat_id", cat_id)
                        if category:
                            sub_cat_name_ = self.sub.get_sub_category("sub_name", sub_cat_name)
                            if not sub_cat_name_:
                                self.sub.update_sub_category(sub_cat_name, cat_id, sub_id)
                                self.response = self.resp.update_response("sub_id", sub_id, "SubCategory")
                            else:
                                self.response = self.resp.already_exist_response("SubCategory", sub_cat_name)
                        else:
                            self.response = self.resp.does_not_exist_response("cat_id", cat_id, "Category")
                    else:
                        self.response = self.resp.does_not_exist_response("sub_id", sub_id, "SubCategory")
                else:
                    self.response = self.resp.invalid_contents_response(
                        is_valid[1])
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response
