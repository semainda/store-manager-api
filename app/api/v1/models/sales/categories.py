"""Module that defines categories model"""

# local imports
from app.db_config.db_setups import DataStuctures
from app.api.v1.models.base import BaseModel


class CategoriesModel(BaseModel):
    """
    Class that represents categories data structure

    The following attributes of categories are stored in this data structure:
        cat_id
        cat_name
    """

    def __init__(self):
        self.categories = DataStuctures().datastructures()[3]
        super().__init__(self.categories, "categories")

    def create_categories(self, *args):
        """Method that creates categories"""
        return self.insert_entries(args)

    def get_category_by_field(self, key, value):
        """Method that returns categories entries by any field"""
        return self.get_entry_by_any_field(key, value)

    def get_category(self, cat_id):
        """Method that returns specific category given role_id"""
        return self.get_entry(cat_id)

    def get_categories(self):
        """Method that returns categories"""
        return self.get_entries()

    def delete_categories(self):
        """Method that deletes categories"""
        return self.delete_entries()

    def update_categories(self, cat_id, **kwargs):
        """Method that updates categories entries given role_id"""
        return self.update_entries(cat_id, kwargs)
