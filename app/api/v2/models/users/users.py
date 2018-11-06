"""This module creates user model and its operations"""
# standard imports
from datetime import datetime

# local imports
from ..models import BaseModel


class UserModel(BaseModel):
    """Class that represent a user"""
    def create_user(self, first_name, last_name, email, user_name, password):
        """Method that creates user while assignind role user"""
        created_date = datetime.now().strftime("%Y, %m, %d")
        sql = """INSERT INTO users(
                first_name, last_name,email,
                user_name, password,
                created_at) VALUES('{}', '{}', '{}', '{}', '{}', '{}')
                RETURNING user_id;""".format(
                    first_name, last_name, email,
                    user_name, password, created_date)
        return self.sql_executer(sql)

    def get_users(self):
        """Method that gets all users"""
        sql ="""SELECT u.user_id, u.first_name, u.last_name, u.email,
                    u.user_name, r.role_name,
                    to_char(created_at, 'YYYY-MM-DD') AS created_at
                FROM users u, roles r, user_roles s
                WHERE s.user_id=u.user_id
                AND s.role_id = r.role_id;"""
        users = self.sql_executer(sql)
        return users

    def get_user(self, key, val):
        """Method for get a specific user"""
        sql ="""SELECT u.user_id, u.first_name, u.last_name, u.email, u.user_name, r.role_name,
                    to_char(created_at, 'YYYY-MM-DD') AS created_at
                FROM users u, roles r, user_roles s
                WHERE s.user_id=u.user_id
                AND s.role_id = r.role_id
                AND U.{}='{}';""".format(key, val)
        user = self.sql_executer(sql)
        if user:
            return user[0]
        return user

    def get_user_login_credentials(self, user_name):
        """Method for get a specific user"""
        sql ="""SELECT u.user_id, u.password, r.role_name
                FROM users u, roles r, user_roles s
                WHERE s.user_id=u.user_id
                AND s.role_id = r.role_id
                AND u.user_name='{}';""".format(user_name)
        credentials = self.sql_executer(sql)
        if credentials:
            return credentials[0]
        return credentials

    def update_user(self, key, val, user_id):
        """Method that updates specific user"""
        sql ="""UPDATE users SET {}='{}'
                WHERE user_id='{}'
                RETURNING user_id;""".format(key, val, user_id)
        return self.sql_executer(sql)

    def delete_user(self, user_id):
        """Method for delete specific user"""
        sql ="""DELETE FROM users WHERE user_id='{}'
                RETURNING user_id;""".format(user_id)
        return self.sql_executer(sql)
