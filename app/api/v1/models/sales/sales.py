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
    """

    def __init__(self):
        self.sales = DataStuctures().datastructures()[6]
        super().__init__(self.sales, "sales")
    
    # Method overide: insert_entries

    def insert_entries(self, **kwargs):
        """Method that overides to do something else"""
        sale_id = ""
        if not self.sales:
            self.sales.extend([kwargs])
            sale_id = kwargs["user_id"]
        else:
            # common k, v lookup
            for data in self.sales:
                match = kwargs.items() & data.items()
                if match:
                    sale_id = kwargs["id"] - 1
                    break
            else:
                self.sales.extend([kwargs])
                sale_id = kwargs["id"]
        return sale_id

    def get_sales_entries(self):
        """Method that return sales"""
        return self.sales
    
    def get_entry_by_any_field(self, k, v):
        """Method that check for a given field and returns it"""
        dt_row = [row for row in self.sales if row[k] == v]
        return dt_row[0]

    def create_sales(self, user_id, sale_date):
        """Method that creates sales"""
        sale_id = len(self.sales) + 1
        return self.insert_entries(
            id=sale_id, user_id=user_id, sale_date=sale_date)

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
        return self.update_entries(sale_id, kwargs)
    
    def get_minimum_allowed(self, available_qty, prod_name):
        """Method that sold_qty against minimum value to be in store"""
        return self.check_for_min_entries(available_qty, prod_name)
