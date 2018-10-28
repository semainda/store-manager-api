"""Module that defines categories endpoints"""
# thirdparty imports
from flask_restful import current_app, Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

# local imports
from app.api.v2.models.sales.categories import CategoriesModel
from app.api.v2.responses.models.base import ModelResponses
from app.api.v2.utils.validators import input_validators


PARSER = reqparse.RequestParser()
PARSER.add_argument(
    "cat_name", required=True, type=str,
    help="Key cat_name is not found or value given is not of required type."
        "Make sure a value is 'string' type")


class Initializer:
    """Method that initializes required classes"""
    @jwt_required
    def __init__(self):
        self.resp = ModelResponses()
        self.cat = CategoriesModel()
        self.response = ""
        self.super_user = current_app.config["DEFAULT_ADMIN"]["role_name"]
        self.loggein_user = get_jwt_identity()["role_name"]


class Categories(Resource, Initializer):
    """Class that creates and ruturn categories"""
    def get(self):
        """Method that return categories"""
        if get_jwt_identity():
            if self.loggein_user == self.super_user:
                categories = self.cat.get_categories()
                if categories:
                    self.response = self.resp.exist_response(categories, "Categories")
                else:
                    self.response = self.resp.does_not_exists_response("Categories")
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response

    def post(self):
        """Method that creates categories"""
        if get_jwt_identity():
            if self.loggein_user == self.super_user:
                data_parsed = PARSER.parse_args()
                cat_name = data_parsed["cat_name"].lower()
                is_valid = input_validators(
                    cat_name=cat_name)
                if is_valid[0]:
                    category = self.cat.get_category("cat_name", cat_name)
                    if not category:
                        self.cat.create_category(cat_name)
                        self.response = self.resp.create_response("Category", cat_name)
                    else:
                        self.response = self.resp.already_exist_response(
                            "Category", cat_name)
                else:
                    self.response = self.resp.invalid_contents_response(
                        is_valid[1])
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response


class CategoriesActivity(Resource, Initializer):
    """Class that handels endpoints that requires unique ids"""
    def get(self, cat_id):
        """Method that returns a category by cat_id"""
        if get_jwt_identity():
            if self.loggein_user == self.super_user:
                category = self.cat.get_category("cat_id", cat_id)
                if category:
                    self.response = self.resp.exist_response(category, "Category")
                else:
                    self.response = self.resp.does_not_exist_response("cat_id", cat_id, "Category")
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response

    def put(self, cat_id):
        """Method that returns a category by cat_id"""
        if get_jwt_identity():
            if self.loggein_user == self.super_user:
                data_parsed = PARSER.parse_args()
                cat_name = data_parsed["cat_name"].lower()
                is_valid = input_validators(cat_name=cat_name)
                if is_valid[0]:
                    category = self.cat.get_category("cat_id", cat_id)
                    if category:
                        cat_name_ = self.cat.get_category("cat_name", cat_name)
                        if not cat_name_:
                            self.cat.update_category(cat_name, cat_id)
                            self.response = self.resp.update_response("cat_id", cat_id, "Category")
                        else:
                            self.response = self.resp.already_exist_response(
                            "Category", cat_name)
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
