"""Module that defines sub_categories model"""

# local imports
from ..models import BaseModel


class SubCategoriesModel(BaseModel):
    """
    Class that represents sub_categories data structure

    The following attributes of sub_categories are stored in this data structure:
        cat_id
        sub_cat_id
        sub_cat_name
    """
    def create_sub_categories(self, sub_name, cat_id):
        """Method that creates sub_categories"""
        sql ="""INSERT INTO sub_categories(sub_name, cat_id)
                VALUES('{}', '{}')
                RETURNING sub_id;""".format(sub_name, cat_id)
        return self.sql_executer(sql)

    def get_sub_category(self, key, val):
        """Method that returns sub_categories entries by any field"""
        sql = "SELECT * FROM sub_categories WHERE {}='{}';".format(key, val)
        sub_category = self.sql_executer(sql)
        if sub_category:
            return sub_category[0]
        return sub_category

    def get_sub_categories(self):
        """Method that returns sub_categories"""
        sql = "SELECT * FROM sub_categories;"
        sub_categories = self.sql_executer(sql)
        return sub_categories

    def update_sub_category(self, sub_name, cat_id, sub_id):
        """Method that updates sub_categories entries given sub_cat_id"""
        sql ="""UPDATE sub_categories SET sub_name='{}', cat_id='{}'
                WHERE sub_id='{}'
                RETURNING sub_name;""".format(sub_name, cat_id, sub_id)
        return self.sql_executer(sql)
        