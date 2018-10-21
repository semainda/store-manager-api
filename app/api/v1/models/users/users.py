"""Module that defines user model"""

# system imports
from datetime import datetime

# local imports
from app.db_config.db_setups import DataStuctures
from app.api.v1.models.base import BaseModel
from app.api.v1.auth.user_auth import UserAuth


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
        super().__init__(self.users, "users")
        self.auth = UserAuth()

    def create_users(self,
                    first_name, last_name, email, user_name, password):
        """Method that creates users"""
        password = self.auth.generate_hash_password(password)
        created_at = datetime.now().strftime("%Y-%m-%d")
        return self.insert_entries(
            first_name, last_name, email, user_name, password, created_at
        )

    def get_users_entries(self):
        """Method that return sales"""
        return self.users
    
    def get_user_by_field(self, key, value):
        """Method that returns user entries by any field"""
        return self.get_entry_by_any_field(key, value)
    
    def get_user(self, user_id):
        """Method that returns specific user given user_id"""
        return self.get_entry(user_id)

    def get_users(self):
        """Method that returns users"""
        return self.get_entries()

    def delete_users(self):
        """Method that deletes users"""
        return self.delete_entries()

    def update_roles(self, user_id, **kwargs):
        """Method that updates users entries given user_id"""
        return self.update_entries(user_id, kwargs)