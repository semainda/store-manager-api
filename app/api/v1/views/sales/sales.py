"""Module that defines sales endpoints"""
# standard imports
from datetime import datetime

# thirdparty imports
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

# local imports
from app.api.v1.auth.user_auth import UserAuth
from app.api.v1.models.sales.products import ProductsModel
from app.api.v1.models.users.users import UserModel
from app.api.v1.models.sales.sales import SalesModel
from app.api.v1.models.sales.sold_products import SoldProductsModel
from app.api.v1.responses.auth.base import AuthResponses
from app.api.v1.responses.validators.base import ValidatorsResponse
from app.api.v1.utils.validators import input_validators

PARSER = reqparse.RequestParser()
PARSER.add_argument(
    "prod_id", required=True, type=int, help="Key prod_id not found")
PARSER.add_argument(
    "quantity", required=True, type=int, help="Key quantity not found")


class Initializer:
    """Method that initializes required classes"""
    def __init__(self):
        self.auth = UserAuth()
        self.resp = AuthResponses()
        self.product = ProductsModel()
        self.user = UserModel()
        self.sale = SalesModel()
        self.sold = SoldProductsModel()
        self.validator = ValidatorsResponse()
        self.sale_date = datetime.now().strftime("%c")
        self.response = ""


class Sales(Resource, Initializer):
    """Class that creates and ruturn sales"""

    @jwt_required
    def get(self):
        """Method that return products"""
        if get_jwt_identity():
            user_id = get_jwt_identity()
            user_role_name = self.auth.return_role_name(user_id)
            if user_role_name == "store_owner":
                # dict list
                sales = self.sale.get_sales_entries()
                if sales:
                    #returns users dict list
                    users = self.user.get_users_entries()
                    # returns sold products dict list
                    sold_products = self.sold.get_sold_products()
                    sales_details = {
                        "Store Manager Sales Details Reports":
                        {user["first_name"].title() + " " +
                        user["last_name"].title() + " Sale Orders": [
                            dict(Sale_ID=sale["id"], Product=product["prod_name"],
                                Qty=product["quantity"],
                                Unit_price=product["price"],
                                Total_price=product["total"],
                                Sales_data=sale["sale_date"]
                            ) for sale in sales 
                                if sale["user_id"] == user["id"]
                                    for product in sold_products
                                        if product["sale_id"] == sale["id"]]
                                            for user in users for user_sale in sales if user["id"] == user_sale["user_id"]
                        }
                    }
                    self.response = sales_details
                else:
                    self.response = self.sale.get_sales()
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response
    
    @jwt_required
    def post(self):
        """Method that creates sale order"""
        if get_jwt_identity():
            user_id = get_jwt_identity()
            user_role_name = self.auth.return_role_name(user_id)
            if user_role_name == "store_attendant":
                data_parsed = PARSER.parse_args()
                prod_id = data_parsed["prod_id"]
                quantity = data_parsed["quantity"]
                is_valid = input_validators(
                    prod_id=prod_id, quantity=quantity)
                if is_valid[0]:
                    product = self.product.get_entry_by_any_field(
                        "id", prod_id)
                    if product:
                        if quantity <= product["quantity"]:
                            qty_remain = product["quantity"] - quantity
                            sale_id = self.sale.create_sales(
                                user_id, self.sale_date)
                            unit_price = product["price"]
                            total_price = unit_price * quantity
                            self.product.update_product_qty(
                                product["id"], qty_remain)
                            self.response = self.sold.create_sold_products(
                                sale_id, product["prod_name"],
                                quantity, unit_price, total_price)
                        else: self.response = self.sale.get_minimum_allowed(
                            product["quantity"], product["prod_name"])
                    else:
                        self.response = self.product.get_product(prod_id)
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
            user_id = get_jwt_identity()
            user_role_name = self.auth.return_role_name(user_id)
            if user_role_name in ("store_owner", "store_attendant"):
                is_valid = input_validators(sale_id=sale_id)
                if is_valid[0]:
                    sale = self.sale.get_sale_by_field("id", sale_id)
                if sale:
                    #returns users dict list
                    user = self.user.get_user_by_field("id", sale["user_id"])
                    # returns sold products dict list
                    sold_products = self.sold.get_sold_products()
                    sales_details = {
                        "Sale Detail Report":
                        {user["first_name"].title() + " " +
                        user["last_name"].title() + " Sale Orders": [
                            dict(Product=product["prod_name"],
                                Qty=product["quantity"],
                                Unit_price=product["price"],
                                Total_price=product["total"],
                                Sales_data=sale["sale_date"]
                            ) for product in sold_products
                                if product["sale_id"] == sale["id"]]
                        }
                    }
                    self.response = sales_details
                else:
                    self.response = self.sale.get_sale(sale_id)
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response
