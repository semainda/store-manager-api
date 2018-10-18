"""Module that defines sub_categories model"""

# local imports
from app.db_config.db_setups import DataStuctures
from app.api.v1.models.base import BaseModel


class SubCategoriesModel(BaseModel):
    """
    Class that represents sub_categories data structure

    The following attributes of sub_categories are stored in this data structure:
        cat_id
        sub_cat_id
        sub_cat_name
    """

    def __init__(self):
        self.sub_categories = DataStuctures().datastructures()[4]
        super().__init__(self.sub_categories, "sub_categories")

    def create_sub_categories(self, *args):
        """Method that creates sub_categories"""
        return self.insert_entries(args)

    def get_sub_category_by_field(self, key, value):
        """Method that returns sub_categories entries by any field"""
        return self.get_entry_by_any_field(key, value)

    def get_sub_category(self, sub_cat_id):
        """Method that returns specific sub_category given sub_cat_id"""
        return self.get_entry(sub_cat_id)

    def get_sub_categories(self):
        """Method that returns sub_categories"""
        return self.get_entries()

    def delete_sub_categories(self):
        """Method that deletes sub_categories"""
        return self.delete_entries()

    def update_sub_categories(self, sub_cat_id, **kwargs):
        """Method that updates sub_categories entries given sub_cat_id"""
        return self.update_entries(sub_cat_id, kwargs)
