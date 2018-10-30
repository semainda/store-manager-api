"""Module that returns validators respons"""

class ValidatorsResponse:
    """Class that defines validators response"""

    def invalid_contents_response(self, key):
            """Method that returns invalid responses"""
            return {
                "Message": "{} value is not of valid type."
                "Make sure a value is not empty and is of valid type".format(
                    key)
                }, 400
