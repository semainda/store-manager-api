"""This module creates user model and its operations"""
# standard imports
from datetime import datetime

# local imports
from ..models import BaseModel
from passlib.hash import pbkdf2_sha256 as hash256


class UserModel(BaseModel):
    """Class that represent a user"""
    def create_user(self, first_name, last_name, email, user_name, password):
        """Method that creates user while assignind role user"""
        created_date = datetime.now().strftime("%Y, %m, %d")
        sql = """INSERT INTO users(
                first_name, last_name,email,
                user_name, password,
                created_at) VALUES(%s, %s, %s, %s, %s, %s) RETURNING user_id;"""
        return self.sql_executer(
            sql, (
                first_name, last_name,
                email, user_name, hash256.hash(password),
                created_date))

    def get_all_users(self):
        """Method that gets all users"""
        sql = "SELECT * FROM users;"
        rows = self.sql_executer(sql)
        users_list = []
        for _, users in enumerate(rows):
            user_id, first_name, last_name,\
                email, user_name, password, created_at = users
            accounts = dict(
                Id=user_id,
                First_name=first_name.upper(),
                Last_name=last_name.upper(),
                Email=email,
                User_name=user_name,
                Password=password,
                Created_date=str(created_at)
            )
            users_list.append(accounts)
        return users_list

    def get_user_by_user_id(self, user_id):
        """Method for get a specific user"""
        sql = "SELECT * FROM users WHERE user_id=%s;"
        row = self.sql_executer(sql, (user_id,))
        user_details = []
        for _, user in enumerate(row):
            user_id, first_name, last_name,\
                email, user_name, password, created_at = user
            account = dict(
                Id=user_id,
                First_name=first_name.upper(),
                Last_name=last_name.upper(),
                Email=email,
                User_name=user_name,
                Password=password,
                Created_date=str(created_at)
            )
            user_details.append(account)
        return user_details

    def get_user_by_user_name_email(self, user_name, email):
        """Method for get a specific user"""
        sql = "SELECT user_name, email FROM users WHERE user_name=%s OR email=%s;"
        return self.sql_executer(sql, (user_name, email))

    def get_user_password_and_id(self, user_name):
        """Method for get a specific user"""
        sql = """SELECT u.user_id, u.password, r.role_name
                FROM users u, user_roles s, roles r 
                WHERE s.user_id=u.user_id
                AND s.role_id=r.role_id AND user_name=%s;"""
        return self.sql_executer(sql, (user_name,))

    def update_user(self, email, password, user_id):
        """Method that updates specific user"""
        sql = """UPDATE users SET email=(%s), password=(%s), user_role=(%s)
                WHERE user_id=(%s) RETURNING user_id;"""
        return self.sql_executer(sql, (email, password, user_id))

    def get_user_role_id(self, user_name):
        sql= """SELECT s.role_id 
                FROM user_roles s, users u
                WHERE s.user_id=u.user_id AND u.user_name=%s;"""
        return self.sql_executer(sql, (user_name, ))
        
    def get_role_name_by_user_id(self, user_id):
        sql="""SELECT r.role_name
                FROM user_roles u, roles r
                WHERE r.role_id=u.role_id AND user_id=%s;"""
        return self.sql_executer(sql, (user_id, ))
    
    

    def delete_user(self, user_id):
        """Method for delete specific user"""
        sql = "DELETE FROM users WHERE user_id=(%s) RETURNING user_id;"
        return self.sql_executer(sql, (user_id,))
