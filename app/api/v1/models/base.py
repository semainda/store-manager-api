"""Module that models data structures"""
# local imports
from app.api.v1.responses.models.base import ModelResponses


class BaseModel(ModelResponses):
    """Class that offers common data structure operations"""
    def __init__(self, dt_name, str_dt_name):
        super().__init__(str_dt_name)
        self.dt_name = dt_name
        self.response = ""

    def insert_entries(self, **kwargs):
        """Method that append entries to a given data structure"""
        # new_entry = [row for row in kwargs]
        if not self.dt_name:
            self.dt_name.extend([kwargs])
            self.response = self.create_response([kwargs])
        else:
            # common k, v lookup
            for data in self.dt_name:
                match = kwargs.items() & data.items()
                if match:
                    exist_values = [dict(match)]
                    self.response = self.already_exist_response(exist_values)
                    break
                # _, val = items
                #exist_values.append(val)
            else:
                self.dt_name.extend([kwargs])
                self.response = self.create_response([kwargs])
        return self.response

    def get_entry(self, entry_id):
        """Method that returns a specific entry of a given data structure"""
        dt_row = [row for row in self.dt_name if row["id"] == entry_id]
        if dt_row:
            self.response = self.exist_response(dt_row[0])
        else:
            self.response = self.does_not_exist_response(entry_id)
        return self.response

    def get_entries(self):
        """Method that return entries of a given data structure"""
        if self.dt_name:
            self.response = self.exists_response(self.dt_name)
        else:
            self.response = self.does_not_exists_response()
        return self.response

    def get_entry_by_any_field(self, k, v):
        """Method that check for a given field and returns it"""
        row_data = ""
        dt_row = [row for row in self.dt_name if row[k] == v]
        if dt_row:
            row_data = dt_row[0]
        else:
            row_data = self.does_not_exist_response(k)
        return row_data

    def update_entries(self, **kwargs):
        """Method that update entries of a data structure"""
        dt_row = [row for row in self.dt_name if row["id"] == kwargs["id"]]
        if not dt_row:
            self.response = self.does_not_exist_response(kwargs["id"])
        # common keys lookup
        match = kwargs.keys() & dt_row[0].keys()
        if match:
            for k in match:
                dt_row[0][k] = kwargs[k]
            self.response = self.update_response(kwargs["id"])
        return self.response

    def delete_entries(self, *args):
        """
            Method that deletes entries of a data structure
            args of the following format is expected
                (1, 2, 3...)
        """
        dt_set = set(v["id"] for _, v in enumerate(self.dt_name))
        entry_set = set(args)
        # common id_key lookups
        match = dt_set & entry_set
        if match == entry_set:
            deleted_entries = []
            for k in match:
                dt_row = [row for row in self.dt_name if row["id"] == k] # returns entry with key k
                entry_index = lambda: self.dt_name.index(dt_row[0])
                poped_item = self.dt_name.pop(entry_index())
                deleted_entries.append(poped_item)
            self.response = self.delete_response(deleted_entries)
        # for more ke_ids more than existing
        else:
            un_exist_id = list(entry_set - match)
            deleted_entries = []
            for k in match:
                dt_row = [row for row in self.dt_name if row["id"] == k] # returns entry with key k
                entry_index = lambda: self.dt_name.index(dt_row[0])
                poped_item = self.dt_name.pop(entry_index())
                deleted_entries.append(poped_item)
            self.response = self.delete_unexist_response(deleted_entries, un_exist_id)
        return self.response

    # sales specific methods that requires responses
    def check_for_min_entries(self, available, prod_name):
        """Method that check for alloweed min and returns it"""
        min_value = 0
        if available == min_value:
            self.response = self.min_value_reached(prod_name)
        else:
            self.response = self.min_value_availabe(prod_name, available)
        return self.response

    def insert_sales(self, **kwargs):
        """Method that append entries to a given data structure"""
        self.dt_name.extend([kwargs])
        self.response = self.create_response([kwargs])
        return self.response