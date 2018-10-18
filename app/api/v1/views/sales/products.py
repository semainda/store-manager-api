"""Module that defines roles endpoints"""
# thirdparty imports
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

# local imports
from app.api.v1.auth.user_auth import UserAuth
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
    "category", required=True, type=str, help="Key cat_id not found")
PARSER.add_argument(
    "sub_category", required=True, type=str, help="Key sub_cat_id not found")
     

class Initializer:
    """Method that initializes required classes"""
    def __init__(self):
        self.auth = UserAuth()
        self.resp = AuthResponses()
        self.product = ProductsModel()
        self.validator = ValidatorsResponse()
        self.response = ""


class Products(Resource, Initializer):
    """Class that creates and ruturn roles"""
    def __init__(self):
        super().__init__()

    @jwt_required
    def post(self):
        """Method that creates roles"""
        if get_jwt_identity():
            user_role_name = self.auth.return_role_name(get_jwt_identity())
            if user_role_name in ("store_owner", "store_attendant"):
                data_parsed = PARSER.parse_args()
                prod_name = data_parsed["prod_name"]
                price = data_parsed["price"]
                quantity = data_parsed["quantity"]
                size = data_parsed["size"]
                category = data_parsed["category"]
                sub_category = data_parsed["sub_category"]
                is_valid = input_validators(
                    prod_name=prod_name, price=price, quantity=quantity,
                    size=size, category=category, sub_category=sub_category)
                if is_valid[0]:
                    self.response = self.product.create_products(
                        prod_name, price, quantity, size,
                        category, sub_category)
                else:
                    self.response = self.validator.invalid_contents_response(is_valid[1])
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response


class ProductsActivity(Resource):
    """Class that handels endpoints that requires unique ids"""
    pass
