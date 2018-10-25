"""Module that handels general models responses"""


class ModelResponses:
    """Class that handels general models responses"""

    def exists_response(self, dt_values, model_name):
        """Method that returns exists response"""
        return {model_name: dt_values}, 200

    def exist_response(self, dt_value, model_name):
        """Method that returns exist response"""
        return {model_name: dt_value}, 200

    def does_not_exists_response(self,  model_name):
        """Method that returns does_not_exists_response"""
        return {"Message": "'{}' does not exists".format(model_name)}, 404

    def does_not_exist_response(self, dt_key, model_name):
        """Method that returns does not exist response"""
        return {
            "Message": "{} with key value '{}' does not exists".format(
                model_name, dt_key)
            }, 404

    def create_response(self, model_name):
        """Method that returns created response"""
        return {
            "Message": "{} created successful".format(model_name)
            }, 201

    def creates_response(self, model_name):
        """Method that returns created response"""
        return {
            "Message": "'{}' created successful".format(
                model_name)
            }, 201

    def already_exist_response(self, model_name):
        """Method that returns exist response """
        return {
            "Message": "{} already exists".format(model_name)
            }, 409

    def update_response(self, dt_id, model_name):
        """Method that returns update response"""
        return {
            "Message": "{} with id '{}' updated successful".format(
                model_name, dt_id)
            }, 201

    def delete_response(self, model_name):
        """Method that returns delete response"""
        return {
            "Message": "{} deleted successful".format(
                model_name)
            }, 200

    def delete_unexist_response(self, values, dt_id, model_name):
        """Method that returns delete response"""
        return {
            "Message": "{} details '{}' deleted successful,\
            While {} with id(s) '{}'\
            not deleted because does not exist".format(
                model_name, values, model_name, dt_id)
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
