"""Module that defines sales model"""

# local imports
from ..models import BaseModel

class SalesModel(BaseModel):
    """
    Class that represents sales data structure

    The following attributes of sales are stored in this data structure:
        sale_id
        user_id
        sale_date
    """
    def create_sale(self, user_id, sale_date, prod_name, sold_qty, price, total):
        """Method that creates meal"""
        sql ="""WITH sale AS(
                    INSERT INTO sales(user_id, sale_date)
                    VALUES(%s, %s) RETURNING sale_id
                )
                INSERT INTO sales_transactions(sale_id, p_id, sold_qty, price, total)
                SELECT sale.p_id, %s, %s, %s, %s FROM sale RETURNING trans_id;"""
        return self.sql_executer(sql, (user_id, sale_date, prod_name, sold_qty, price, total))


    def get_sales(self):
        """Method that return sales"""
        sql = """SELECT * FROM sales"""
        rows = self.sql_executer(sql)
        sales_list = []
        for _, items in enumerate(rows):
            sale_id, user_id, date = items
            display = dict(
                sale_id=sale_id,
                user_id=user_id,
                date=date
                )
            sales_list.append(display)
        return sales_list
    
    def get_sale_by_id(self, sale_id):
        """Method that check for a given field and returns it"""
        sql = """SELECT * FROM sales WHERE sale_id=%s"""
        return self.sql_executer(sql, (sale_id, ))

    def get_minimum_allowed(self, available_qty, prod_name):
        """Method that sold_qty against minimum value to be in store"""
        return self.check_for_min_entries(available_qty, prod_name)

