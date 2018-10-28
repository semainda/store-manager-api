"""Module that defines sales endpoints"""
# standard imports
from datetime import datetime

# thirdparty imports
from flask_restful import current_app, Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

# local imports
from app.api.v2.models.sales.products import ProductsModel
from app.api.v2.models.sales.product_status import ProductSatatusModel
from app.api.v2.models.users.users import UserModel
from app.api.v2.models.sales.sales import SalesModel
from app.api.v2.responses.models.base import ModelResponses
from app.api.v2.utils.validators import input_validators

PARSER = reqparse.RequestParser()
PARSER.add_argument(
    "prod_id", required=True, type=int,
    help="Key prod_id is not found or value given is not of required type."
        "Make sure a value is 'integer type")
PARSER.add_argument(
    "quantity", required=True, type=int,
    help="Key quantity is not found or value given is not of required type."
        "Make sure a value is 'integer' type")


class Initializer:
    """Method that initializes required classes"""
    @jwt_required
    def __init__(self):
        self.product = ProductsModel()
        self.status = ProductSatatusModel()
        self.user = UserModel()
        self.sale = SalesModel()
        self.resp = ModelResponses()
        self.attendant = current_app.config["DEFAULT_ATTENDANT"]
        self.super_user = current_app.config["DEFAULT_ADMIN"]["role_name"]
        self.loggein_user = get_jwt_identity()["role_name"]
        self.sale_date = datetime.now().strftime("%Y, %m, %d")
        self.response = ""


class Sales(Resource, Initializer):
    """Class that creates and ruturn sales"""
    def get(self):
        """Method that return products"""
        if get_jwt_identity():
            if self.loggein_user == self.super_user:
                # dict list
                sales = self.sale.get_sales()
                if sales:
                    self.response = self.resp.exists_response(sales, "Sales")
                else:
                    self.response = self.resp.does_not_exists_response("Sales")
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response

    def post(self):
        """Method that creates sale order"""
        if get_jwt_identity():
            if self.loggein_user == self.attendant:
                data_parsed = PARSER.parse_args()
                prod_id = data_parsed["prod_id"]
                quantity = data_parsed["quantity"]
                is_valid = input_validators(
                    prod_id=prod_id, quantity=quantity)
                if is_valid[0]:
                    product = self.product.get_product("p_id", prod_id)
                    if product:
                        status = self.status.get_product_status(
                            "p_id", prod_id)
                        available = status["stock_qty"] - status["sold_qty"]
                        if available != 0:
                            if quantity <= available:
                                user_id = get_jwt_identity()["user_id"]
                                qty_remain = product["qty"] - quantity
                                self.sale.create_sale(user_id, prod_id,
                                    quantity, self.sale_date)
                                self.product.update_product(prod_id, qty_remain)
                                self.status.update_product_status(
                                    quantity, prod_id)
                                self.response = self.resp.create_response(
                                    "Sale", product["prod_name"])
                            else: self.response = self.resp.min_value_availabe(
                                product["prod_name"], available)
                        else:
                            self.response = self.resp.min_value_reached(product["prod_name"])
                    else:
                        self.response = self.resp.does_not_exist_response("prod_id", prod_id, "Product")
                else:
                    self.response = self.resp.invalid_contents_response(
                        is_valid[1])
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response


class SalesActivity(Resource, Initializer):
    """Class that defines methods for specific sale order"""
    def get(self, user_id):
        """Method that returns a specific sale order"""
        if get_jwt_identity():
            if self.loggein_user == self.super_user:
                sales = self.sale.get_sale("user_id", user_id)
                if sales:
                    self.response = self.resp.exist_response(sales, "Sales")
                else:
                    self.response = self.resp.does_not_exists_response("Sales")
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response


class UserSales(Resource, Initializer):
    """Class that returns specific user sales"""
    def get(self):
        """Method that return products"""
        if get_jwt_identity():
            if self.loggein_user == self.attendant:
                # dict list
                user_id = get_jwt_identity()["user_id"]
                sales = self.sale.get_sale("user_id", user_id)
                if sales:
                    self.response = self.resp.exists_response(
                        sales, "Sales Details")
                else:
                    self.response = self.resp.does_not_exists_response("Sales")
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response


class UserSalesActivity(Resource, Initializer):
    """Class that returns specific user sales"""
    def get(self, sale_id):
        """Method that return products"""
        if get_jwt_identity():
            if self.loggein_user == self.attendant:
                # dict list
                user_id = get_jwt_identity()["user_id"]
                sales = self.sale.get_sale("user_id", user_id)
                if sales:
                    sale = [ sale for sale in sales if sale["trans_id"] == sale_id]  
                    self.response = self.resp.exist_response(sale, "Sale")
                else:
                    self.response = self.resp.does_not_exists_response("Sale")
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response
