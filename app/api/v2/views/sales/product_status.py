"""Module that defines products_status endpoints"""
# thirdparty imports
from flask_restful import current_app, Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

# local imports
from app.api.v2.models.sales.product_status import ProductSatatusModel
from app.api.v2.models.sales.products import ProductsModel
from app.api.v2.responses.models.base import ModelResponses
from app.api.v2.utils.validators import input_validators


class Initializer:
    """Method that initializes required classes"""
    @jwt_required
    def __init__(self):
        self.resp = ModelResponses()
        self.status = ProductSatatusModel()
        self.product = ProductsModel
        self.response = ""
        self.super_user = current_app.config["DEFAULT_ADMIN"][0]
        self.loggein_user = get_jwt_identity()["role_name"]


class ProductStatus(Resource, Initializer):
    """Class that creates and ruturn products_status"""
    def get(self):
        """Method that return categories"""
        if get_jwt_identity():
            if self.loggein_user == self.super_user:
                products_status = self.status.get_products_status()
                if products_status:
                    self.response = self.resp.exist_response(products_status, "Products_status")
                else:
                    self.response = self.resp.does_not_exists_response("Products_status")
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response


class ProductStatusActivity(Resource, Initializer):
    def get(self, prod_id):
        """Method that returns a Product_status by prod_id"""
        if get_jwt_identity():
            if self.loggein_user == self.super_user:
                product_status = self.status.get_product_status("p_id", prod_id)
                if product_status:
                    self.response = self.resp.exist_response(product_status, "Product_status")
                else:
                    self.response = self.resp.does_not_exist_response("prod_id", prod_id, "Product_status")
            else:
                self.response = self.resp.forbidden_user_access_response()
        else:
            self.response = self.resp.unauthorized_user_access_responses()
        return self.response
