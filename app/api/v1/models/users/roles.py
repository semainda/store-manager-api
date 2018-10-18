"""Module that defines roles model"""

# local imports
from app.db_config.db_setups import DataStuctures
from app.api.v1.models.base import BaseModel


class RoleModel(BaseModel):
    """
    Class that represents roles data structure

    The following attributes of roles are stored in this data structure:
        role_id
        role_name
    """

    def __init__(self):
        self.roles = DataStuctures().datastructures()[0]
        super().__init__(self.roles, "roles")

    def create_roles(self, role_name):
        """Method that creates roles"""
        role_id = len(self.roles) + 1
        return self.insert_entries(role_id=role_id, role_name=role_name)

    def get_role_by_field(self, key, value):
        """Method that returns roles entries by any field"""
        return self.get_entry_by_any_field(key, value)

    def get_role(self, role_id):
        """Method that returns specific role given role_id"""
        return self.get_entry(role_id)

    def get_roles(self):
        """Method that returns roles"""
        return self.get_entries()

    def delete_roles(self):
        """Method that deletes roles"""
        return self.delete_entries()

    def update_roles(self, role_id, **kwargs):
        """Method that updates roles entries given role_id"""
        return self.update_entries(role_id, kwargs)
