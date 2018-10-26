"""Module that defines products model"""

# local imports
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

    def create_product(self, prod_name, price, quantity, size, cat_id, sub_cat_id):
        """Method that creates meal"""
        sql ="""WITH product AS(
                    INSERT INTO products(prod_name, price, qty, size, cat_id, sub_id)
                    VALUES(%s, %s, %s, %s, %s, %s) RETURNING p_id, qty
                )
                INSERT INTO product_status(p_id, stock_qty)
                SELECT product.p_id, product.qty FROM product RETURNING stock_qty;"""
        return self.sql_executer(sql, (
            prod_name, price, quantity, size, cat_id, sub_cat_id))

    def get_product_by_name(self, prod_name):
        """Method that returns existing meal name"""
        sql = "SELECT * FROM products WHERE prod_name=%s;"
        return self.sql_executer(sql, (prod_name,))

    def get_product_by_id(self, p_id):
        """Method that returns a specific meal"""
        sql = """SELECT * FROM products WHERE p_id=%s;"""
        return self.sql_executer(sql, (p_id,))

    def get_all_products(self):
        """Method that returns a list of meals available"""
        sql = """SELECT * FROM products;"""
        rows = self.sql_executer(sql)
        products_list = []
        for _, items in enumerate(rows):
            p_id, prod_name, price, quantity, size, cat_id, sub_cat_id = items
            display = dict(
                Id=p_id,
                Name=prod_name.upper(),
                Price="TZS " + str(price),
                Qty=quantity,
                Size=size,
                Category=cat_id,
                Sub_cat=sub_cat_id
                )
            products_list.append(display)
        return products_list

    def update_product_quantity(self, p_id, quantity):
        """Method that update all meal entries"""
        sql = """UPDATE products SET quantity=(%s)
                WHERE p_id=(%s) RETURNING p_id;"""
        return self.sql_executer(sql, (p_id, quantity))

    