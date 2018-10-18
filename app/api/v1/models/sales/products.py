"""Module that defines products model"""

# local imports
from app.db_config.db_setups import DataStuctures
from app.api.v1.models.base import BaseModel


class ProductsModel(BaseModel):
    """
    Class that represents products data structure

    The following attributes of products are stored in this data structure:
        prod_id
        prod_name
        quantity
        price
        size
        cat_id
        sub_cat_id
        mfd_date
        exp_date
    """

    def __init__(self):
        self.products = DataStuctures().datastructures()[5]
        super().__init__(self.products, "products")

    def create_products(self, *args):
        """Method that creates products"""
        return self.insert_entries(args)

    def get_product_by_field(self, key, value):
        """Method that returns products entries by any field"""
        return self.get_entry_by_any_field(key, value)

    def get_product(self, prod_id):
        """Method that returns specific product given prod_id"""
        return self.get_entry(prod_id)

    def get_products(self):
        """Method that returns products"""
        return self.get_entries()

    def delete_products(self):
        """Method that deletes products"""
        return self.delete_entries()

    def update_products(self, prod_id, **kwargs):
        """Method that updates categories entries given prod_id"""
        return self.update_entries(prod_id, kwargs)
