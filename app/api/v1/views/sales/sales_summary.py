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
        self.sale_date = datetime.now().strftime("%Y-%m-%d")
        self.response = ""


class SalesSummary(Resource, Initializer):
    """Class that ruturn sales summary for all store attendant"""

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
                    sales_details ={user["first_name"].title() + " " +
                        user["last_name"].title() + " Sale Orders": [
                            dict(Qty=product["quantity"],
                                Price=product["total"],
                                Date=sale["sale_date"]
                            ) for sale in sales 
                                if sale["user_id"] == user["id"]
                                    for product in sold_products
                                        if product["sale_id"] == sale["id"]]
                                            for user in users
                    }
                    # Generating Sales Summary Report
                    sales_summary = {
                        "Total Number of Sales Records Created": 0,
                        "Total Number of Products Sold": 0,
                        "Total Worth of Products Sold": 0, "Sale Date": ""}
                    for attendant in sales_details:
                        for orders in sales_details[attendant]:
                            sales_summary[
                                "Total Number of Sales Records Created"] += 1
                            sales_summary[
                                "Total Number of Products Sold"] += orders["Qty"]
                            sales_summary[
                                "Total Worth of Products Sold"] += orders["Price"]
                            sales_summary["Sale Date"] = orders["Date"]
                    report = {
                        "Store Manager Sales Summary Reports":
                        {attendant: [sales_summary]}
                        }
                    self.response = report
                else:
                    self.response = self.sale.get_sales()
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response


class UserSalesSummary(Resource, Initializer):
    """Method that return user specific sales orders"""
    @jwt_required
    def get(self, user_id):
        """Method that returns a specific sale order"""
        if get_jwt_identity():
            user_id_ = get_jwt_identity()
            user_role_name = self.auth.return_role_name(user_id_)
            if user_role_name == "store_owner":
                sale = self.sale.get_sale_by_field("user_id", user_id)
                if sale:
                    #returns users dict list
                    user = self.user.get_user_by_field("id", user_id)
                    # returns sold products dict list
                    sold_products = self.sold.get_sold_products()
                    sales_details = {user["first_name"].title() + " " +
                        user["last_name"].title() + " Sale Orders": [
                            dict(Qty=product["quantity"],
                                Price=product["total"],
                                Date=sale["sale_date"]
                            ) for product in sold_products
                                if product["sale_id"] == sale["id"]]
                        }
                    # Generating Sales Summary Report
                    sales_summary = {
                        "Total Number of Sales Records Created": 0,
                        "Total Number of Products Sold": 0,
                        "Total Worth of Products Sold": 0, "Sale Date": ""}
                    for attendant in sales_details:
                        for orders in sales_details[attendant]:
                            sales_summary[
                                "Total Number of Sales Records Created"] += 1
                            sales_summary[
                                "Total Number of Products Sold"] += orders["Qty"]
                            sales_summary[
                                "Total Worth of Products Sold"] += orders["Price"]
                            sales_summary["Sale Date"] = orders["Date"]
                    report = {
                        "Store Manager Sales Summary Reports":
                        {attendant: [sales_summary]}
                        }
                    self.response = report
                else:
                    self.response = self.sale.get_sale(user_id)
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response

class SalesSummaryActivity(Resource, Initializer):
    """Class that defines methods for specific sale order"""
    @jwt_required
    def get(self):
        """Method that returns a specific sale order"""
        if get_jwt_identity():
            user_id = get_jwt_identity()
            user_role_name = self.auth.return_role_name(user_id)
            if user_role_name == "store_owner":
                sale = self.sale.get_sale_by_field("user_id", user_id)
                if sale:
                    #returns users dict list
                    user = self.user.get_user_by_field("id", user_id)
                    # returns sold products dict list
                    sold_products = self.sold.get_sold_products()
                    sales_details = {user["first_name"].title() + " " +
                        user["last_name"].title() + " Sale Orders": [
                            dict(Qty=product["quantity"],
                                Price=product["total"],
                                Date=sale["sale_date"]
                            ) for product in sold_products
                                if product["sale_id"] == sale["id"]]
                        }
                    # Generating Sales Summary Report
                    sales_summary = {
                        "Total Number of Sales Records Created": 0,
                        "Total Number of Products Sold": 0,
                        "Total Worth of Products Sold": 0, "Sale Date": ""}
                    for attendant in sales_details:
                        for orders in sales_details[attendant]:
                            sales_summary[
                                "Total Number of Sales Records Created"] += 1
                            sales_summary[
                                "Total Number of Products Sold"] += orders["Qty"]
                            sales_summary[
                                "Total Worth of Products Sold"] += orders["Price"]
                            sales_summary["Sale Date"] = orders["Date"]
                    report = {
                        "Store Manager Sales Summary Reports":
                        {attendant: [sales_summary]}
                        }
                    self.response = report
                else:
                    self.response = self.sale.get_sale(user_id)
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response
