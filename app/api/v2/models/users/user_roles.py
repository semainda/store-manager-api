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
    
    def create_user_roles(self, role_id, user_id):
        """Method that creates user_roles"""
        sql = """INSERT INTO user_roles VALUES(%s, %s) RETURNING role_id;"""
        return self.sql_executer(sql, (role_id, user_id))
        
    def get_user_role(self, role_id):
        """Method that returns specific user_role given user_role_id"""
        sql = """SELECT user_id FROM user_roles WHERE role_id=%s;"""
        return self.sql_executer(sql, (role_id, ))

    def get_user_role_by_id(self, user_id):
        """Method that returns specific user_role given user_role_id"""
        sql = """SELECT role_id FROM user_roles WHERE user_id=%s;"""
        return self.sql_executer(sql, (user_id, ))

    def get_user_roles(self):
        """Method that returns user_roles"""
        sql = """SELECT * FROM user_roles;"""
        return self.sql_executer(sql)

    def update_user_roles(self, user_id, role_id):
        """Method that updates user_roles entries given user_role_id"""
        sql = """UPDATE user_roles SET role_id=%s WHERE user_id=%s RETURNING role_id;"""
        return self.sql_executer(sql, (user_id, role_id))


