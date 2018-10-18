"""Module that returns validators respons"""

class ValidatorsResponse:
    """Class that defines validators response"""

    def invalid_contents_response(self, key):
            """Method that returns invalid responses"""
            return {
                "Message": "{} is invalid for it to be created".format(
                    key)
                }, 400