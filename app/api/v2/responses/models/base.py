"""Module that handels general models responses"""
from app.api.v2.responses.auth.base import AuthResponses
from app.api.v2.responses.validators.base import ValidatorsResponse


class ModelResponses(AuthResponses, ValidatorsResponse):
    """Class that handels general models responses"""

    def exists_response(self, dt_values, model_name):
        """Method that returns exists response"""
        return {model_name: dt_values}, 200

    def exist_response(self, dt_value, model_name):
        """Method that returns exist response"""
        return {model_name: dt_value}, 200

    def does_not_exists_response(self, model_name):
        """Method that returns does_not_exists_response"""
        return {"Message": "'{}' are not yet created".format(model_name)}, 404

    def does_not_exist_response(self, key_name, key_val, model_name):
        """Method that returns does not exist response"""
        return {
            "Message": "{} '{}: {}' does not exists".format(
                model_name, key_name, key_val)
            }, 404

    def create_response(self, model_name, value):
        """Method that returns created response"""
        return {
            "Message": "{} '{}' created successful".format(model_name, value)
            }, 201

    def creates_response(self, model_name, value):
        """Method that returns created response"""
        return {
            "Message": "{} '{}' created successful".format(
                model_name, value)
            }, 201

    def already_exist_response(self, model_name, value):
        """Method that returns exist response """
        return {
            "Message": "{} '{}' already exists".format(model_name, value)
            }, 409

    def update_response(self, key_name, key_val, model_name):
        """Method that returns update response"""
        return {
            "Message": "{} '{}: {}' updated successful".format(
                model_name, key_name, key_val)
            }, 200

    def delete_response(self, key_name, key_val, model_name):
        """Method that returns delete response"""
        return {
            "Message": "{} '{}: {}' deleted successful".format(
                model_name, key_name, key_val)
            }, 200
    
    def min_value_reached(self, prod_name):
        """Method that returns mini reached response"""
        return {
            "Message":
            "Sorry this product '{}' is out of stock for now."
            "Try again when new stock has arraived".format(
                prod_name)
            }, 209

    def min_value_availabe(self, prod_name, available):
        """Method that return available for sale"""
        return {
            "Message":
            "This product '{}' has only '{}' items in stock."
            "So sale order should not exceed this value".format(
                prod_name, available)
            }, 209
    def primary_foregn_key_does_not_match(self, primary, foregin):
        """Method that return foreign does not match response"""
        return {
            "Message":
            "'{}' does not belong to '{}' not found".format(primary, foregin)}, 404
