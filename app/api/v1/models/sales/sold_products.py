"""Module that defines sold_products model"""

# local imports
from app.db_config.db_setups import DataStuctures
from app.api.v1.models.base import BaseModel


class SoldProductsModel(BaseModel):
    """
    Class that represents sold_products data structure

    The following attributes of sold_products are stored in this data structure:
        sold_prod_id
        sale_id
        prod_id
        sold_qty
        price
        total
    """

    def __init__(self):
        self.sold_products = DataStuctures().datastructures()[7]
        super().__init__(self.sold_products, "Sale Orders")

    # method overide
    def get_entries(self):
        """Method that return sales"""
        return self.sold_products

    def create_sold_products(self, sale_id, prod_name, qty, price, total):
        """Method that creates sold_products"""
        return self.insert_sales(
            sale_id=sale_id, prod_name=prod_name,
            quantity=qty, price=price, total=total)

    def get_sold_product_by_field(self, key, value):
        """Method that returns sold_products entries by any field"""
        return self.get_entry_by_any_field(key, value)

    def get_sold_product(self, sold_prod_id):
        """Method that returns specific sales given sold_prod_id"""
        return self.get_entry(sold_prod_id)

    def get_sold_products(self):
        """Method that returns sold_products"""
        return self.get_entries()
