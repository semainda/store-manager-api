"""Module that defines sales endpoints"""
# standard imports
from datetime import datetime

# thirdparty imports
from flask_restful import current_app, Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

# local imports
from app.api.v2.models.sales.products import ProductsModel
from app.api.v2.models.users.users import UserModel
from app.api.v2.models.sales.sales import SalesModel
from app.api.v2.responses.models.base import ModelResponses
from app.api.v2.utils.validators import input_validators


class Initializer:
    """Method that initializes required classes"""
    @jwt_required
    def __init__(self):
        self.product = ProductsModel()
        self.user = UserModel()
        self.sale = SalesModel()
        self.resp = ModelResponses()
        self.sale_date = datetime.now().strftime("%Y-%m-%d")
        self.super_user = current_app.config["DEFAULT_ADMIN"]["role_name"]
        self.attendant = current_app.config["DEFAULT_ATTENDANT"]
        self.loggein_user = get_jwt_identity()["role_name"]
        self.response = ""


class StoreSalesSummary(Resource, Initializer):
    """Class that handles store sales summary"""
    def get(self):
        """Method that returns store sales summary"""
        if get_jwt_identity():
            if self.loggein_user == self.super_user:
                # dict list
                sales = self.sale.get_sales()
                if sales:
                    # Generating Sales Summary Report
                    sales_summary = {
                        "Total Number of Sales Records Created": 0,
                        "Total Number of Products Sold": 0,
                        "Total Worth of Products Sold": 0, "Sale Date": ""}
                    # for attendant in sales_details:
                    for orders in sales:
                        sales_summary[
                            "Total Number of Sales Records Created"] += 1
                        sales_summary[
                            "Total Number of Products Sold"] += orders["sold_qty"]
                        sales_summary[
                            "Total Worth of Products Sold"] += orders["total"]
                        sales_summary["Sale Date"] = orders["sale_date"]
                    report = {
                        "Store Sales Summary Reports": [sales_summary]
                        }
                    self.response = report
                else:
                    self.response = self.resp.does_not_exists_response("Sales")
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response


class SalesSummary(Resource, Initializer):
    """Class that ruturn sales summary for all store attendant"""
    def get(self):
        """Method that return products"""
        if get_jwt_identity():
            if self.loggein_user == self.super_user:
                # dict list
                sales = self.sale.get_sales()
                if sales:
                    # Generating Sales Summary Report
                    seles_users = self.sale.get_sale_users()

                    sales_details =[{user["first_name"].title() + " " +
                        user["last_name"].title() + " Sale Orders": [
                            dict(
                                trans_id=user_sale["trans_id"],
                                sold_qty=user_sale["sold_qty"],
                                total_sales=user_sale["total"],
                                sale_date=user_sale["sale_date"]
                            ) for user_sale in sales if user_sale["user_id"] == user["user_id"]]
                        } for user in seles_users]


                    """sales_summary = {
                        "Total Number of Sales Records Created": 0,
                        "Total Number of Products Sold": 0,
                        "Total Worth of Products Sold": 0, "Sale Date": ""}
                    # for attendant in sales_details:
                    for orders in sales:
                        sales_summary[
                            "Total Number of Sales Records Created"] += 1
                        sales_summary[
                            "Total Number of Products Sold"] += orders["sold_qty"]
                        sales_summary[
                            "Total Worth of Products Sold"] += orders["total"]
                        sales_summary["Sale Date"] = orders["sale_date"]
                    report = {
                        "Store Manager Sales Summary Reports": [sales_summary]
                        }"""
                    self.response = sales_details
                else:
                    self.response = self.resp.does_not_exists_response("Sales")
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response


class SalesSummaryActivity(Resource, Initializer):
    """Class that defines methods for specific sale order"""
    def get(self, user_id):
        """Method that returns a specific sale order"""
        if get_jwt_identity():
            if self.loggein_user == self.super_user:
                sale = self.sale.get_sale("user_id", user_id)
                if sale:
                    #returns users dict list
                    user = self.user.get_user("user_id", user_id)
                    sales_details = {user["first_name"].title() + " " +
                        user["last_name"].title() + " Sale Orders": [
                            dict(
                                sold_qty=user_sale["sold_qty"],
                                total_sales=user_sale["total"],
                                sale_date=user_sale["sale_date"]
                            ) for user_sale in sale]
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
                                "Total Number of Products Sold"] += orders["sold_qty"]
                            sales_summary[
                                "Total Worth of Products Sold"] += orders["total_sales"]
                            sales_summary["Sale Date"] = orders["sale_date"]
                    report = {
                        "Store Manager Sales Summary Reports":
                        {attendant: [sales_summary]}
                        }
                    self.response = report
                else:
                    self.response = self.resp.does_not_exist_response("user_id", user_id, "Sales")
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response


class UserSalesSummary(Resource, Initializer):
    """Method that return user specific sales orders"""
    def get(self):
        """Method that returns a specific sale order"""
        if get_jwt_identity():
            user_id = get_jwt_identity()["user_id"]
            if self.loggein_user == self.attendant:
                sale = self.sale.get_sale("user_id", user_id)
                print(sale)
                if sale:
                    #returns users dict list
                    user = self.user.get_user("user_id", user_id)
                    sales_details = {user["first_name"].title() + " " +
                        user["last_name"].title() + " Sale Orders": [
                            dict(
                                sold_qty=user_sale["sold_qty"],
                                total_sales=user_sale["total"],
                                sale_date=user_sale["sale_date"]
                            ) for user_sale in sale]
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
                                "Total Number of Products Sold"] += orders["sold_qty"]
                            sales_summary[
                                "Total Worth of Products Sold"] += orders["total_sales"]
                            sales_summary["Sale Date"] = orders["sale_date"]
                    report = {
                        "Store Manager Sales Summary Reports":
                        {attendant: [sales_summary]}
                        }
                    self.response = report
                else:
                    self.response = self.resp.does_not_exist_response(user_id, "Sales")
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response
