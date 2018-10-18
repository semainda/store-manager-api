"""Module that defines user_roles model"""

# local imports
from app.db_config.db_setups import DataStuctures
from app.api.v1.models.base import BaseModel


class UserRoleModel(BaseModel):
    """
    Class that represents user_roles data structure

    The following attributes of user_roles are stored in this data structure:
        user_role_id
        role_id
        user_id
    """

    def __init__(self):
        self.user_roles = DataStuctures().datastructures()[2]
        super().__init__(self.user_roles, "user_roles")

    def create_user_roles(self, *args):
        """Method that creates user_roles"""
        return self.insert_entries(args)

    def get_user_role_by_field(self, key, value):
        """Method that returns user_roles entries by any field"""
        return self.get_entry_by_any_field(key, value)

    def get_user_role(self, user_role_id):
        """Method that returns specific user_role given user_role_id"""
        return self.get_entry(user_role_id)
    
    def get_role_user(self, user_id):
        """Method that returns specific user_role given user_id"""
        return self.get_entry(user_id)

    def get_user_roles(self):
        """Method that returns user_roles"""
        return self.get_entries()

    def delete_user_roles(self):
        """Method that deletes user_roles"""
        return self.delete_entries()

    def update_user_roles(self, user_role_id, **kwargs):
        """Method that updates user_roles entries given user_role_id"""
        return self.update_entries(user_role_id, kwargs)
