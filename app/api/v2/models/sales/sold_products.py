"""Module that defines sold_products model"""

# local imports
from ..models import BaseModel


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

    def get_sold_product_by_field(self, key, value):
        """Method that returns sold_products entries by any field"""
        pass

    def get_sold_product(self, sold_prod_id):
        """Method that returns specific sales given sold_prod_id"""
        pass

    def get_sold_products(self):
        """Method that returns sold_products"""
        sql = """SELECT * FROM sales_transactions"""
        return self.sql_executer(sql)
        
