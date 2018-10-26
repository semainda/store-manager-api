"""Module that defines roles endpoints"""
# thirdparty imports
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

# local imports
from app.api.v2.models.sales.categories import CategoriesModel
from app.api.v2.models.sales.sub_categories import SubCategoriesModel
from app.api.v2.models.sales.products import ProductsModel
from app.api.v2.responses.models.base import ModelResponses
from app.api.v2.responses.auth.base import AuthResponses
from app.api.v2.responses.validators.base import ValidatorsResponse
from app.api.v2.utils.validators import input_validators


PARSER = reqparse.RequestParser()
PARSER.add_argument(
    "prod_name", required=True, type=str, help="Key prod_name not found")
PARSER.add_argument(
    "price", required=True, type=int, help="Key price not found")
PARSER.add_argument(
    "quantity", required=True, type=int, help="Key quantity not found")
PARSER.add_argument(
    "size", required=True, type=int, help="Key size not found")
PARSER.add_argument(
    "cat_id", required=True, type=int, help="Key cat_id not found")
PARSER.add_argument(
    "sub_cat_id", required=True, type=int, help="Key sub_cat_id not found")
     

class Initializer:
    """Method that initializes required classes"""
    def __init__(self):
        self.resp = AuthResponses()
        self.cat = CategoriesModel()
        self.sub = SubCategoriesModel()
        self.modresp = ModelResponses()
        self.product = ProductsModel()
        self.validator = ValidatorsResponse()
        self.response = ""


class Products(Resource, Initializer):
    """Class that creates and ruturn roles"""
    @jwt_required
    def get(self):
        """Method that return products"""
        if get_jwt_identity():
            user_ = get_jwt_identity()
            if user_["role_name"] in ("store_owner", "store_attendant"):
                products = self.product.get_all_products()
                if products:
                    self.response = self.modresp.exists_response(products, "Products")
                else:
                    self.response = self.modresp.does_not_exists_response("Products")
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response


    @jwt_required
    def post(self):
        """Method that creates products"""
        if get_jwt_identity():
            user_ = get_jwt_identity()
            if user_["role_name"] in ("store_owner", "store_attendant"):
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
                    category = self.cat.get_category_by_id(cat_id)
                    if category:
                        sub_category = self.sub.get_sub_category_by_id(cat_id)
                        if sub_category:
                            if sub_category[0][0] == sub_cat_id:

                                self.product.create_product(
                                        prod_name, price, quantity, size,
                                        cat_id, sub_cat_id)
                                self.response = self.modresp.create_response("Product")
                            else:
                               self.response = {"Message": "cat_id and sub_id do not match"}, 400 
                        else:
                            self.response = self.modresp.does_not_exist_response(cat_id, "SubCategory")
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


class ProductsActivity(Resource, Initializer):
    """Class that handels endpoints that requires unique ids"""
    @jwt_required
    def get(self, prod_id):
        """Method that returns a product by product_id"""
        if get_jwt_identity():
            user_ = get_jwt_identity()
            if user_["role_name"] in ("store_owner", "store_attendant"): 
                product = self.product.get_product_by_id(prod_id)
                if product:
                    self.response = self.modresp.exist_response(product, "Product")
                else:
                    self.response = self.modresp.does_not_exist_response(prod_id, "Product")
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response
