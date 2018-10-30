"""Module that creates category model"""
# local imports
from ..models import BaseModel


class CategoriesModel(BaseModel):
    """
    Class that represents a category of the meal

    The following attributes of a category are stored in this table:
        category id
        category name
    """
    def create_category(self, cat_name):
        """Method that create category"""
        sql ="""INSERT INTO categories(cat_name) VALUES('{}')
                RETURNING cat_name;""".format(cat_name)
        return self.sql_executer(sql)

    def get_category(self, key, val):
        """Method that returns a specific category"""
        sql = "SELECT * FROM categories WHERE {}='{}';".format(key, val)
        category = self.sql_executer(sql)
        if category:
            return category[0]
        return category

    def get_categories(self):
        """Method that returns a list of categories"""
        sql = "SELECT * FROM categories;"
        categories = self.sql_executer(sql)
        return categories

    def update_category(self, cat_name, cat_id):
        """Method that update specific category"""
        sql ="""UPDATE categories SET cat_name='{}' WHERE cat_id='{}' 
                RETURNING cat_name;""".format(cat_name, cat_id)
        return self.sql_executer(sql)

    def delete_category(self, cat_id):
        """Method that delete specific category"""
        sql ="""DELETE FROM categories WHERE cat_id='{}'
                RETURNING cat_name CASCADE;""".format(cat_id)
        return self.sql_executer(sql)
