"""Module that defines sales model"""

# local imports
from app.db_config.db_setups import DataStuctures
from app.api.v1.models.base import BaseModel


class SalesModel(BaseModel):
    """
    Class that represents sales data structure

    The following attributes of sales are stored in this data structure:
        sale_id
        user_id
        sale_date
        price
    """

    def __init__(self):
        self.sales = DataStuctures().datastructures()[6]
        super().__init__(self.sales, "sales")

    def create_sales(self, *args):
        """Method that creates sales"""
        return self.insert_entries(args)

    def get_sale_by_field(self, key, value):
        """Method that returns sales entries by any field"""
        return self.get_entry_by_any_field(key, value)

    def get_sale(self, sale_id):
        """Method that returns specific sales given sale_id"""
        return self.get_entry(sale_id)

    def get_sales(self):
        """Method that returns sales"""
        return self.get_entries()

    def delete_sales(self):
        """Method that deletes sales"""
        return self.delete_entries()

    def update_sales(self, sale_id, **kwargs):
        """Method that updates sales entries given sale_id"""
        return self.update_entries(prod_id, kwargs)
