"""Module that defines users authorizations"""
# thirdparty imports
from flask_jwt_extended import create_access_token
from passlib.hash import pbkdf2_sha256 as hash256
from app.db_config.db_setups import DataStuctures


class UserAuth:
    """Class that defines users authorization"""
    def __init__(self):
        self.roles = DataStuctures().datastructures()[0]
        self.user_roles = DataStuctures().datastructures()[2]

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

    def return_role_name(self, user_id):
        """Method that returns logged in user role_name"""
        response = ""
        role_id = [row for row in self.user_roles if row["user_id"] == user_id]
        if role_id:
            role_name = [
                row for row in self.roles if row["id"] == role_id[0]["role_id"]
                ]
            if role_name:
                response = role_name[0]["role_name"]
            else:
                response = role_name
        else:
            response = role_id 
        return response