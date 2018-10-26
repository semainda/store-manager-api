"""Module that defines user_roles model"""

# local imports
from ..models import BaseModel


class UserRoleModel(BaseModel):
    """
    Class that represents user_roles data structure

    The following attributes of user_roles are stored in this data structure:
        user_role_id
        role_id
        user_id
    """
    
    # Method overide
    def create_user_roles(self, role_id, user_id):
        """Method that creates user_roles"""
        pass

    def get_user_role_by_field(self, key, value):
        """Method that returns user_roles entries by any field"""
        pass

    def get_user_role(self, role_id):
        """Method that returns specific user_role given user_role_id"""
        sql = """SELECT user_id FROM user_roles WHERE role_id=%s"""
        return self.sql_executer(sql, (role_id, ))

    def get_user_roles(self):
        """Method that returns user_roles"""
        pass

    def delete_user_roles(self):
        """Method that deletes user_roles"""
        pass

    def update_user_roles(self, user_role_id, role_id):
        """Method that updates user_roles entries given user_role_id"""
        pass
