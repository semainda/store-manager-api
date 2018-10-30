"""Module that defines products model"""

# local imports
from ..models import BaseModel


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
    """

    def create_product(self, prod_name, qty, size, price, cat_id, sub_id):
        """Method that creates products"""
        sql ="""WITH product AS(
                    INSERT INTO products(
                        prod_name, qty, size, price, cat_id, sub_id)
                    VALUES('{}', '{}', '{}', '{}', '{}', '{}'
                    ) RETURNING p_id, qty
                )
                INSERT INTO product_status(p_id, stock_qty)
                SELECT product.p_id, product.qty
                FROM product RETURNING p_id;""".format(
                    prod_name, qty, size, price, cat_id, sub_id)
        return self.sql_executer(sql)

    def get_product(self, key, val):
        """Method that returns existing product"""
        sql ="SELECT * FROM products WHERE {}='{}';".format(key, val)
        product = self.sql_executer(sql)
        if product:
            return product[0]
        return product

    def get_products(self):
        """Method that returns a list of products available"""
        sql = """SELECT * FROM products;"""
        products = self.sql_executer(sql)
        return products

    def update_product(self, p_id, qty):
        """Method that update all productsentries"""
        sql = """UPDATE products SET qty='{}'
                WHERE p_id='{}' RETURNING p_id;""".format(qty, p_id)
        return self.sql_executer(sql)

    