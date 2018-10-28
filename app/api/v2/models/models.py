"""Module that creates model for all models class"""
from app.db_config.store_db_setups import DatabaseOperations


class BaseModel:
    """
        Class that offers crud operations
    """
    def __init__(self):
        self.conn = DatabaseOperations().db_con()

    def sql_executer(self, sql_query):
        """
            Method that performs read operations to return rows
        """
        with self.conn:
            with self.conn.cursor() as curr:
                curr.execute(sql_query)
                rows = curr.fetchall()
        return rows
