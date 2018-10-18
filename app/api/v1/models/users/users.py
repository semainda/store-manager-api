"""Module that defines user model"""

# system imports
from datetime import datetime

# local imports
from .....db_config.db_setups import DataStuctures
from app.api.v1.models.base import BaseModel
from ...auth.user_auth import UserAuth


class UserModel(BaseModel):
    """
    Class that represents users data structure

    The following attributes of users are stored in this data structure:
        user_id
        first_name
        last_name
        email
        user_name
        password
        created_at
    """

    def __init__(self):
        self.users = DataStuctures().datastructures()[1]
        super().__init__(self.users)
        self.auth = UserAuth()

    def create_user(self,
                    first_name, last_name, email, user_name, password):
        """Method that creates users"""
        password = self.auth.generate_hash_password(password)
        created_at = datetime.now().strftime("%Y-%m-%d")
        return self.insert_entries(
            first_name, last_name, email, user_name, password, created_at
        )

    def get_user_by_field(self, key, value):
        """Method that returns user entries by any field"""
        return self.get_entry_by_any_field(key, value)
