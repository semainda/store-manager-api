"""Module that defines users authorizations"""
# thirdparty imports
from flask_jwt_extended import create_access_token
from passlib.hash import pbkdf2_sha256 as hash256


class UserAuth:
    """Class that defines users authorization"""

    def generate_hash_password(self, password):
        """ Method that generate hashed password"""
        return hash256.hash(password)

    def verify_hashed_password(self, loggedin_password, current_password):
        """
            Method that verify the hashed agains loggedin password,
            returns true if match found otherwise false
        """
        return hash256.verify(loggedin_password, current_password)

    def return_access_token(self, token_identity):
        """Method that creates and returns user access token"""
        return create_access_token(identity=token_identity)
