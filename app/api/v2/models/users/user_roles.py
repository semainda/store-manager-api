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
        sql ="""INSERT INTO user_roles(role_id, user_id) VALUES('{}', '{}')
                RETURNING role_id;""".format(role_id, user_id)
        return self.sql_executer(sql)

    def get_user_role(self, key, val):
        """Method that returns specific user_role given user_role_id"""
        sql = """SELECT * FROM user_roles WHERE {}='{}';""".format(key, val)
        user_role = self.sql_executer(sql)
        return user_role

    def get_user_roles(self):
        """Method that returns user_roles"""
        sql = """SELECT * FROM user_roles;"""
        return self.sql_executer(sql)

    def update_user_roles(self, user_id, role_id):
        """Method that updates user_roles entries given user_role_id"""
        sql ="""UPDATE user_roles SET role_id='{}' WHERE user_id='{}'
                RETURNING user_id;""".format(role_id, user_id)
        return self.sql_executer(sql)
