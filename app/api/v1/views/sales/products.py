"""Module that defines roles endpoints"""
# thirdparty imports
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

# local imports
from app.api.v1.auth.user_auth import UserAuth
from app.api.v1.models.sales.categories import CategoriesModel
from app.api.v1.models.sales.sub_categories import SubCategoriesModel
from app.api.v1.models.sales.products import ProductsModel
from app.api.v1.responses.auth.base import AuthResponses
from app.api.v1.responses.validators.base import ValidatorsResponse
from app.api.v1.utils.validators import input_validators


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
        self.auth = UserAuth()
        self.resp = AuthResponses()
        self.cat = CategoriesModel()
        self.sub = SubCategoriesModel()
        self.product = ProductsModel()
        self.validator = ValidatorsResponse()
        self.response = ""


class Products(Resource, Initializer):
    """Class that creates and ruturn roles"""
    def __init__(self):
        super().__init__()
    
    @jwt_required
    def get(self):
        """Method that return products"""
        if get_jwt_identity():
            user_role_name = self.auth.return_role_name(get_jwt_identity())
            if user_role_name in ("store_owner", "store_attendant"):
                self.response = self.product.get_products()
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response



    @jwt_required
    def post(self):
        """Method that creates products"""
        if get_jwt_identity():
            user_role_name = self.auth.return_role_name(get_jwt_identity())
            if user_role_name in ("store_owner", "store_attendant"):
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
                    category = self.cat.get_entry_by_any_field("id", cat_id)
                    if category:
                        sub_category = self.sub.get_entry_by_any_field(
                            "id", sub_cat_id)
                        if sub_category:
                            # if category["cat_id"] == sub_category["cat_id"]:
                                self.response = self.product.create_products(
                                    prod_name, price, quantity, size,
                                    cat_id, sub_cat_id)
                            # else:
                                # self.response = {
                                   #  "Message":
                                    # "Product category and it's sub_category are not related"
                                    # }, 400
                        else:
                            self.response = self.sub.get_sub_category(
                                sub_cat_id)
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


class ProductsActivity(Resource, Initializer):
    """Class that handels endpoints that requires unique ids"""
    @jwt_required
    def get(self, prod_id):
        """Method that returns a product by product_id"""
        if get_jwt_identity():
            user_role_name = self.auth.return_role_name(get_jwt_identity())
            if user_role_name in ("store_owner", "store_attendant"):
                self.response = self.product.get_product(prod_id)
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response
