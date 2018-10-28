"""Module that creates product_status model"""
# local imports
from ..models import BaseModel


class ProductSatatusModel(BaseModel):
    """
    Class that represents a category of the meal

    The following attributes of a category are stored in this table:
        category id
        category name
    """

    def get_product_status(self, key, val):
        """Method that returns a specific products_status"""
        sql = "SELECT * FROM product_status WHERE {}='{}';".format(key, val)
        product_status = self.sql_executer(sql)
        if product_status:
            return product_status[0]
        return product_status

    def get_products_status(self):
        """Method that returns a list of products_status"""
        sql ="""SELECT p.p_id, p.prod_name, s.stock_qty, s.sold_qty,
                (s.stock_qty - s.sold_qty) AS current_stock_qty
                FROM product_status s, products p
                WHERE s.p_id = p.p_id;"""
        products_status = self.sql_executer(sql)
        return products_status

    def update_product_status(self, sold_qty, p_id):
        """Method that update specific products_status"""
        sql ="""UPDATE product_status SET sold_qty= sold_qty + {}
                WHERE p_id='{}'
                RETURNING p_id;""".format(sold_qty, p_id)
        return self.sql_executer(sql)
