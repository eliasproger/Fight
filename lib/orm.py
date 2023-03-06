import sqlite3
from typing import Union, List


class SQLiteORM:
    def __init__(self, database_name):
        self.sqlite_connection = sqlite3.connect(database_name)
        self.cursor = self.sqlite_connection.cursor()

    def update(self, table_name, set_columns, where_columns):
        set_string = "".join([f"\"{key}\" = '{value}', " for key, value in set_columns.items()])[:-2]
        search_string = "WHERE " + "".join([f"\"{key}\" = '{value}' and " for key, value in where_columns.items()])[:-4]
        search_string = search_string if search_string != "WHERE " else ""
        req = f"UPDATE \"{table_name}\" SET {set_string} {search_string}"
        self.cursor.execute(req)

    def insert(self, table_name: str, new_values: tuple):
        req = f"INSERT INTO {table_name} VALUES{new_values};"
        self.cursor.execute(req)

    def delete(self, table_name, where_columns):
        search_string = "WHERE " + "".join([f"\"{key}\" = '{value}' and " for key, value in where_columns.items()])[:-4]
        search_string = search_string if search_string != "WHERE " else ""
        req = f"DELETE FROM {table_name} {where_columns}"
        self.cursor.execute(req)

    def select(self, table_name: str, columns: Union[str, List[str]]):
        req = f"SELECT {', '.join(columns) if type(columns) == list else columns} FROM {table_name};"
        self.cursor.execute(req)
        return self.cursor.fetchall()
