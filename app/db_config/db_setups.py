"""Module that initializes data storage structures"""
# standard imports
from datetime import datetime

# thirdparty imports
from passlib.hash import pbkdf2_sha256 as hash256
from termcolor import colored


class DataStuctures:
    """Class that creates data storage stuctures"""
    roles = []
    users = []
    user_roles = []
    categories = []
    sub_categories = []
    products = []
    sales = []
    sold_products = []
    
    def init_db(self):
        """Method that creates store data structures"""
        self.roles
        self.users
        self.user_roles
        self.categories
        self.sub_categories
        self.products
        self.sales
        self.sold_products

    def datastructures(self):
        """Method that returns created store data structures"""
        db = [
            self.roles,
            self.users,
            self.user_roles,
            self.categories,
            self.sub_categories,
            self.products,
            self.sales,
            self.sold_products
        ]
        return db

    def create_default_admin(self, *args):
        """Method that creates default store admin"""
        created_at = datetime.now().strftime("%Y-%m-%d")
        data = args[0]
        self.roles.append(
            dict(
                role_id=1,
                role_name=data[0]
                )
            )
        self.users.append(
            dict(
                user_id=1,
                first_name=data[1],
                last_name=data[2],
                email=data[3],
                user_name=data[4],
                password=hash256.hash((data[5])),
                created_at=created_at
                )
            )
        self.user_roles.append(
            dict(
                user_id=self.users[0]["user_id"],
                role_id=self.roles[0]["role_id"])
            )
        return colored(" * Store Owner: {}".format(self.users[0]["user_name"]), "green")
