"""Module that defines sales endpoints"""
# standard imports
from datetime import datetime

# thirdparty imports
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

# local imports
from app.api.v2.models.sales.products import ProductsModel
from app.api.v2.models.users.users import UserModel
from app.api.v2.models.sales.sales import SalesModel
from app.api.v2.models.sales.sold_products import SoldProductsModel
from app.api.v2.responses.auth.base import AuthResponses
from app.api.v2.responses.models.base import ModelResponses
from app.api.v2.responses.validators.base import ValidatorsResponse
from app.api.v2.utils.validators import input_validators

PARSER = reqparse.RequestParser()
PARSER.add_argument(
    "prod_id", required=True, type=int, help="Key prod_id not found")
PARSER.add_argument(
    "quantity", required=True, type=int, help="Key quantity not found")


class Initializer:
    """Method that initializes required classes"""
    def __init__(self):
        self.resp = AuthResponses()
        self.product = ProductsModel()
        self.user = UserModel()
        self.sale = SalesModel()
        self.sold = SoldProductsModel()
        self.modresp = ModelResponses()
        self.validator = ValidatorsResponse()
        self.sale_date = datetime.now().strftime("%Y, %m, %d")
        self.response = ""


class Sales(Resource, Initializer):
    """Class that creates and ruturn sales"""

    @jwt_required
    def get(self):
        """Method that return products"""
        if get_jwt_identity():
            user_ = get_jwt_identity()
            if user_["role_name"] == "store_owner":
                # dict list
                sales = self.sale.get_sales()
                if sales:
                    #returns users dict list
                    users = self.user.get_all_users()
                    # returns sold products dict list
                    sold_products = self.sold.get_sold_products()
                    sales_details = {
                        "Store Manager Sales Details Reports":
                        {user[1].title() + " " +
                        user[2].title() + " Sale Orders": [
                            dict(Sale_ID=sale[0], Product=product[3],
                                Qty=product[4],
                                Unit_price=product[5],
                                Total_price=product[6],
                                Sales_data=sale[2]
                            ) for sale in sales 
                                if sale[1] == user[0]
                                    for product in sold_products
                                        if product[1] == sale[0]]
                                            for user in users for user_sale in sales if user[0] == user_sale[1]
                        }
                    }
                    self.response = sales_details
                else:
                    self.response = self.modresp.does_not_exists_response("Sales")
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response
    
    @jwt_required
    def post(self):
        """Method that creates sale order"""
        if get_jwt_identity():
            user_ = get_jwt_identity()
            if user_["role_name"] == "store_attendant":
                data_parsed = PARSER.parse_args()
                prod_id = data_parsed["prod_id"]
                quantity = data_parsed["quantity"]
                is_valid = input_validators(
                    prod_id=prod_id, quantity=quantity)
                if is_valid[0]:
                    product = self.product.get_product_by_id(prod_id)
                    if product:
                        if quantity <= product[2]:
                            qty_remain = product[2] - quantity
                            total_price = product[4] * quantity
                            sale = self.sale.reate_sale(self, user_["user_id"], self.sale_date, product[1], quantity, product[4], total_price)
                            if sale:
                                self.product.update_product_qty(
                                prod_id, qty_remain)
                                self.response = self.modresp.create_response("Sale")
                        else: self.response = self.sale.get_minimum_allowed(
                            product[2], product[1])
                    else:
                        self.response = self.modresp.does_not_exist_response(prod_id, "Product")
                else:
                    self.response = self.validator.invalid_contents_response(
                        is_valid[1])
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response


class SalesActivity(Resource, Initializer):
    """Class that defines methods for specific sale order"""
    @jwt_required
    def get(self, sale_id):
        """Method that returns a specific sale order"""
        if get_jwt_identity():
            user_ = get_jwt_identity()
            if user_["role_name"] in ("store_owner", "store_attendant"):
                is_valid = input_validators(sale_id=sale_id)
                if is_valid[0]:
                    sale = self.sale.get_sale_by_id(sale_id)
                if sale:
                    #returns users dict list
                    user = self.user.get_user_by_user_id(sale[1])
                    # returns sold products dict list
                    sold_products = self.sold.get_sold_products()
                    sales_details = {
                        "Sale Detail Report":
                        {user[1].title() + " " +
                        user[2].title() + " Sale Orders": [
                            dict(Product=product[1],
                                Qty=product[4],
                                Unit_price=product[5],
                                Total_price=product[6],
                                Sales_data=sale[2]
                            ) for product in sold_products
                                if product[1] == sale[0]]
                        }
                    }
                    self.response = sales_details
                else:
                    self.response = self.modresp.does_not_exist_response(sale_id, "Sale")
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response
