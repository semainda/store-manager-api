"""Module that handels general models responses"""


class ModelResponses:
    """Class that handels general models responses"""

    def __init__(self, dt_name):
        self.name = str(dt_name)[:-1]
        self.names = str(dt_name)

    def exists_response(self, dt_values):
        """Method that returns exists response"""
        return {"{}: {}".format(self.names, dt_values)}, 200

    def exist_response(self, dt_value):
        """Method that returns exist response"""
        return {"{}: {}".format(self.name, dt_value)}, 200

    def does_not_exists_response(self):
        """Method that returns does_not_exists_response"""
        return {"Message": "'{}' does not exists".format(self.names)}, 404

    def does_not_exist_response(self, dt_id):
        """Method that returns does not exist response"""
        return {
            "Message": "{} with id '{}' does not exists".format(
                self.name, dt_id)
            }, 404

    def create_response(self, name):
        """Method that returns created response"""
        return {
            "Message": "{} named '{}' created successful".format(
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

    def invalid_contents_response(self, name):
        """Method that returns invalid responses"""
        return {
            "Message": "{} '{}' is invalid for it to be created".format(
                self.name, name)
            }, 400

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
