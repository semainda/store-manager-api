"""Module that handels general models responses"""


class ModelResponses:
    """Class that handels general models responses"""

    def __init__(self, str_dt_name):
        self.name = str_dt_name[:-1]
        self.names = str_dt_name

    def exists_response(self, dt_values):
        """Method that returns exists response"""
        return {self.names: "{}".format(dt_values)}, 200

    def exist_response(self, dt_value):
        """Method that returns exist response"""
        return {self.name: "{}".format(dt_value)}, 200

    def does_not_exists_response(self):
        """Method that returns does_not_exists_response"""
        return {"Message": "'{}' does not exists".format(self.names)}, 404

    def does_not_exist_response(self, dt_key):
        """Method that returns does not exist response"""
        return {
            "Message": "{} with key value '{}' does not exists".format(
                self.name, dt_key)
            }, 404

    def create_response(self, name):
        """Method that returns created response"""
        return {
            "Message": "{}: '{}' created successful".format(
                self.name, name)
            }, 201

    def creates_response(self):
        """Method that returns created response"""
        return {
            "Message": "'{}' created successful".format(
                self.names)
            }, 201

    def already_exist_response(self, values):
        """Method that returns exist response """
        return {
            "Message": "{} with value(s) '{}' already exists".format(
                self.name, values)
            }, 409

    def update_response(self, dt_id):
        """Method that returns update response"""
        return {
            "Message": "{} with id '{}' updated successful".format(
                self.name, dt_id)
            }, 201

    def delete_response(self, values):
        """Method that returns delete response"""
        return {
            "Message": "{} details '{}' deleted successful".format(
                self.name, values)
            }, 200

    def delete_unexist_response(self, values, dt_id):
        """Method that returns delete response"""
        return {
            "Message": "{} details '{}' deleted successful,\
            While {} with id(s) '{}'\
            not deleted because does not exist".format(
                self.name, values, self.names, dt_id)
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
