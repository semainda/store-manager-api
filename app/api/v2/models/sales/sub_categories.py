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
        sql = "INSERT INTO sub_categories(sub_name, cat_id) VALUES(%s, %s) RETURNING sub_name;"
        return self.sql_executer(sql, (sub_name, cat_id))

    def get_sub_category_by_id(self, cat_id):
        """Method that returns sub_categories entries by any field"""
        sql = "SELECT sub_name FROM sub_categories WHERE cat_id=%s;"
        return self.sql_executer(sql, (cat_id,))
        

    def get_sub_category_name(self, sub_name):
        """Method that returns specific sub_category given sub_cat_id"""
        sql = "SELECT * FROM sub_categories WHERE sub_name=%s;"
        return self.sql_executer(sql, (sub_name,))
       

    def get_all_sub_categories(self):
        """Method that returns sub_categories"""
        sql = "SELECT * FROM sub_categories;"
        rows = self.sql_executer(sql)
        categories = []
        for _, items in enumerate(rows):
            sub_id, sub_name, cat_id = items
            category = dict(
                Id=sub_id,
                Name=sub_name.upper(),
                Category=cat_id
            )
            categories.append(category)
        return categories

    def update_sub_categories(self, sub_name, cat_id):
        """Method that updates sub_categories entries given sub_cat_id"""
        sql = "UPDATE sub_categories SET sub_name=(%s)\
            WHERE cat_id=(%s) RETURNING sub_name;"
        return self.sql_executer(sql, (sub_name, cat_id))
        