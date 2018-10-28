"""Module that creates role model"""
# local imports
from ..models import BaseModel


class RoleModel(BaseModel):
    """
    Class that represents a role

    The following attributes of a role are stored in this table:
        role id
        role name
    """
    def create_role(self, role_name):
        """Method that create role"""
        sql ="""INSERT INTO roles(role_name) VALUES('{}')
                RETURNING role_id;""".format(role_name)
        return self.sql_executer(sql)

    def get_role(self, key, val):
        """Method that returns a specific role"""
        sql = "SELECT * FROM roles WHERE {}='{}';".format(key, val)
        role = self.sql_executer(sql)
        if role:
            return role[0]
        return role

    def get_roles(self):
        """Method that returns a list of roles"""
        sql = "SELECT * FROM roles;"
        roles = self.sql_executer(sql)
        return roles

    def update_role(self, role_name, role_id):
        """Method that update specific role"""
        sql ="""UPDATE roles SET role_name='{}'
                WHERE role_id='{}'
                RETURNING role_id;""".format(role_name, role_id)
        return self.sql_executer(sql)

    def delete_role(self, key, val):
        """Method that delete specific role"""
        sql ="""DELETE FROM roles WHERE {}='{}'
                RETURNING role_name;""".format(key, val)
        return self.sql_executer(sql)

