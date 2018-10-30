"""Module that defines sales_transactions model"""

# local imports
from ..models import BaseModel

class SalesModel(BaseModel):
    """
    Class that represents sales_transactions

    The following attributes of sales are stored in this data structure:
        sale_id
        user_id
        sale_date 
    """
    def create_sale(self, user_id, p_id, sold_qty, sale_date):
        """Method that creates sales_transactions"""
        sql ="""INSERT INTO sales_transactions(
                user_id, p_id, sold_qty, sale_date)
                VALUES('{}', '{}', '{}', '{}')
                RETURNING trans_id""".format(
                    user_id, p_id, sold_qty, sale_date)
        return self.sql_executer(sql)

    def get_sales(self):
        """Method that return sales_transactions"""
        sql = """
            SELECT s.trans_id, s.user_id, p.prod_name, p.price, s.sold_qty,
                (p.price * s.sold_qty) AS total, to_char(s.sale_date, 'YYYY-MM-DD') AS sale_date
            FROM products p, sales_transactions s
            WHERE s.p_id = p.p_id
            ORDER BY sale_date;"""
        sales = self.sql_executer(sql)
        return sales
    
    def get_sale(self, key, val):
        """Method that check for a given field and returns it"""
        sql ="""SELECT s.trans_id, s.user_id, p.prod_name, p.price, s.sold_qty,
                (p.price * s.sold_qty) AS total, to_char(s.sale_date, 'YYYY-MM-DD') AS sale_date
            FROM products p, sales_transactions s
            WHERE s.p_id = p.p_id
            AND s.{}='{}'
            ORDER BY sale_date;""".format(key, val)
        sale = self.sql_executer(sql)
        return sale
    
    def get_sale_users(self):
        """Method that returns unique list of sales users"""
        sql ="""SELECT DISTINCT s.user_id, u.first_name, u.last_name
                FROM sales_transactions s, users u
                WHERE s.user_id = u.user_id;"""
        return self.sql_executer(sql)
