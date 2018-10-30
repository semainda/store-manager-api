"""Module that defines roles endpoints"""
# thirdparty imports
from flask_restful import current_app, Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

# local imports
from app.api.v2.models.sales.categories import CategoriesModel
from app.api.v2.models.sales.sub_categories import SubCategoriesModel
from app.api.v2.models.sales.products import ProductsModel
from app.api.v2.responses.models.base import ModelResponses
from app.api.v2.utils.validators import input_validators


PARSER = reqparse.RequestParser()
PARSER.add_argument(
    "prod_name", required=True, type=str, 
    help="Key prod_name is not found or value given is not of required type."
        "Make sure a value is 'string' type")
PARSER.add_argument(
    "price", required=True, type=int,
    help="Key price is not found or value given is not of required type."
        "Make sure a value is 'integer' type")
PARSER.add_argument(
    "quantity", required=True, type=int,
    help="Key quantity is not found or value given is not of required type."
        "Make sure a value is 'integer' type")
PARSER.add_argument(
    "size", required=True, type=int,
    help="Key size is not found or value given is not of required type."
        "Make sure a value is 'integer' type")
PARSER.add_argument(
    "cat_id", required=True, type=int,
    help="Key cat_id is not found or value given is not of required type."
        "Make sure a value is 'integer' type")
PARSER.add_argument(
    "sub_cat_id", required=True, type=int,
    help="Key sub_cat_id is not found or value given is not of required type."
        "Make sure a value is 'integer' type")


class Initializer:
    """Method that initializes required classes"""
    @jwt_required
    def __init__(self):
        self.cat = CategoriesModel()
        self.sub = SubCategoriesModel()
        self.resp = ModelResponses()
        self.product = ProductsModel()
        self.response = ""
        self.attendant = current_app.config["DEFAULT_ATTENDANT"]
        self.super_user = current_app.config["DEFAULT_ADMIN"][0]
        self.loggein_user = get_jwt_identity()["role_name"]


class Products(Resource, Initializer):
    """Class that creates and ruturn roles"""
    def get(self):
        """Method that return products"""
        if get_jwt_identity():
            if self.loggein_user in (self.super_user, self.attendant):
                products = self.product.get_products()
                if products:
                    self.response = self.resp.exists_response(products, "Products")
                else:
                    self.response = self.resp.does_not_exists_response("Products")
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response

    def post(self):
        """Method that creates products"""
        if get_jwt_identity():
            if self.loggein_user in (self.super_user, self.attendant):
                data_parsed = PARSER.parse_args()
                prod_name = data_parsed["prod_name"].lower()
                price = data_parsed["price"]
                quantity = data_parsed["quantity"]
                size = data_parsed["size"]
                cat_id = data_parsed["cat_id"]
                sub_cat_id = data_parsed["sub_cat_id"]
                is_valid = input_validators(
                    prod_name=prod_name, price=price, quantity=quantity,
                    size=size, cat_id=cat_id, sub_cat_id=sub_cat_id)
                if is_valid[0]:
                    product = self.product.get_product("prod_name", prod_name)
                    if not product:
                        category = self.cat.get_category("cat_id", cat_id)
                        if category:
                            sub_category = self.sub.get_sub_category(
                                "sub_id", sub_cat_id)
                            if sub_category:
                                if sub_category["cat_id"] == cat_id:
                                    self.product.create_product(
                                            prod_name, quantity, size, price,
                                            cat_id, sub_cat_id)
                                    self.response = self.resp.create_response(
                                        "Product", prod_name)
                                else:
                                    self.response = self.\
                                    resp.primary_foregn_key_does_not_match(
                                        "sub_id: " + str(sub_cat_id), "cat_id: " + str(cat_id))
                            else:
                                self.response = self.resp.does_not_exist_response(
                                    "sub_id", sub_cat_id, "SubCategory")
                        else:
                            self.response = self.resp.does_not_exist_response(
                                "cat_id", cat_id, "Category")
                    else:
                        self.response = self.resp.already_exist_response("Product", prod_name)
                else:
                    self.response = self.resp.invalid_contents_response(
                        is_valid[1])
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response


class ProductsActivity(Resource, Initializer):
    """Class that handels endpoints that requires unique ids"""
    def get(self, prod_id):
        """Method that returns a product by product_id"""
        if get_jwt_identity():
            if self.loggein_user in (self.super_user, self.attendant): 
                product = self.product.get_product("p_id", prod_id)
                if product:
                    self.response = self.resp.exist_response(
                        product, "Product")
                else:
                    self.response = self.resp.does_not_exist_response(
                        "prod_id", prod_id, "Product")
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response
