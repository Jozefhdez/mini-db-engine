'''
In-Memory Storage with B-Tree Indexing explanation

Data Structure:

storage.tables: dict storing table schemas and rows
  Example: {
    "users": {
      "columns": ["id", "name", "age"],
      "rows": [
        {"id": 5, "name": "Alice", "age": 25}, # index 0
        {"id": 2, "name": "Bob", "age": 30}, # index 1
        {"id": 8, "name": "Charlie", "age": 35} # index 2
      ],
      "index_column": "id"
    }
  }

storage.indexes: dict of B-Trees for fast lookups
  Example: {
    "users": BTree with keys [2, 5, 8] -> values [1, 0, 2]
  }
  The B-Tree maps: key (id value) -> row_index (position in rows array)
'''

from btree import BTree
import json
import os

class Storage:
    def __init__(self, filename="db.json"):
        self.filename = filename
        self.tables = {}
        self.indexes = {}
        if os.path.exists(filename):
            with open(filename, "r") as f:
                self.tables = json.load(f) # deserialize json back into py object

    def save(self):
        '''
        Open file in write mode and serialize the entire self.tables to json.
        '''
        with open(self.filename, "w") as f:
            json.dump(self.tables, f, indent=2)

    def create_table(self, name, columns, index_column=None):
        '''
        Create a new table schema and optionally set up a B-Tree index.
        '''
        self.tables[name] = {
            "columns": columns,
            "rows": [],
            "index_column": index_column
        }
        if index_column:
            self.indexes[name] = BTree(t=3)
        self.save()

    def insert_row(self, name, values):
        '''
        Insert new row into table and update index if one exists.
        '''
        table = self.tables[name]
        row = dict(zip(table["columns"], values))
        # Example: columns=["id", "name", "age"], values=[1, "Alice", 25]
        # Result: {"id": 1, "name": "Alice", "age": 25}
        table["rows"].append(row)
        idx = len(table["rows"]) - 1

        index_col = table["index_column"]
        if index_col:
            key = row[index_col]
            self.indexes[name].insert(key, idx)
        self.save()

    def select_all(self, name):
        '''
        Return all rows.
        '''
        return self.tables[name]["rows"]

    def select_where_indexed(self, name, column, value):
        '''
        Attempt indexed lookup, returns matching row in a list, empty list if not found, or None if the column isn't indexed.
        '''
        table = self.tables[name]
        if not (table["index_column"] == column and name in self.indexes):
            return None # not indexed
        row_idx = self.indexes[name].search(self.indexes[name].root, value)
        if row_idx is not None:
            return [table["rows"][row_idx]] # return as list of 1 row
        return [] # not found

    def delete_where(self, name, column, value):
        '''
        Delete all rows where column equals value and rebuild the index.

        honestly I rather create a fresh b-tree than do the b-ree deletion implementation lmfao, but if u wanna do that go for it king
        '''
        table = self.tables[name]
        table["rows"] = [r for r in table["rows"] if str(r[column]) != str(value)] # keep only rows that dont match
        
        # Rebuild index if table has one
        if table["index_column"] and name in self.indexes:
            index_col = table["index_column"]
            self.indexes[name] = BTree(t=3)  # create fresh B-Tree
            for idx, row in enumerate(table["rows"]):
                key = row[index_col]
                self.indexes[name].insert(key, idx)  # re-insert with updated indices
        
        self.save()