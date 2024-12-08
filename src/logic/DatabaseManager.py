import sqlite3

class DatabaseManager:
    def __init__(self, db_path):
        """
        Initialize the DatabaseManager with the database file path.
        """
        self.db_path = db_path
        self.connection = None
        self.cursor = None

    def connect(self):
        """
        Establishes a connection to the SQLite database.
        """
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()

    def disconnect(self):
        """
        Closes the connection to the SQLite database.
        """
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None

    def execute(self, query, params=()):
        """
        Executes a given SQL query with optional parameters.

        :param query: The SQL query to execute.
        :param params: Tuple of parameters to use with the query.
        """
        try:
            self.connect()
            self.cursor.execute(query, params)
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            self.disconnect()

    def fetchall(self, query, params=()):
        """
        Executes a SELECT query and fetches all results.

        :param query: The SELECT SQL query to execute.
        :param params: Tuple of parameters to use with the query.
        :return: List of tuples containing the query results.
        """
        try:
            self.connect()
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return []
        finally:
            self.disconnect()

    def fetchone(self, query, params=()):
        """
        Executes a SELECT query and fetches all results.

        :param query: The SELECT SQL query to execute.
        :param params: Tuple of parameters to use with the query.
        :return: List of tuples containing the query results.
        """
        try:
            self.connect()
            self.cursor.execute(query, params)
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return []
        finally:
            self.disconnect()

    def create(self, table, data):
        """
        Inserts a new row into a specified table.

        :param table: Name of the table.
        :param data: Dictionary of column-value pairs to insert.
        """
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        self.execute(query, tuple(data.values()))

    def read(self, table, columns=None, conditions=None, one=False):
        """
        Reads rows from a specified table with optional conditions.

        :param table: Name of the table.
        :param columns: List of columns to retrieve (e.g., ["col1", "col2"]).
                        If None, retrieves all columns.
        :param conditions: Dictionary of column-value pairs for filtering.
                        If None, retrieves all rows.
        :return: List of rows matching the conditions.
        """
        columns_clause = ", ".join(columns) if columns else "*"
        query = f"SELECT {columns_clause} FROM {table}"

        if conditions:
            where_clause = " AND ".join([f"{col} = ?" for col in conditions.keys()])
            query += f" WHERE {where_clause}"
            return self.fetchall(query, tuple(conditions.values())) if not one else self.fetchone(query, tuple(conditions.values()))

        return self.fetchall(query) if not one else self.fetchone(query)

    def update(self, table, data, conditions):
        """
        Updates rows in a specified table based on conditions.

        :param table: Name of the table.
        :param data: Dictionary of column-value pairs to update.
        :param conditions: Dictionary of column-value pairs for filtering.
        """
        set_clause = ", ".join([f"{col} = ?" for col in data.keys()])
        where_clause = " AND ".join([f"{col} = ?" for col in conditions.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        self.execute(query, tuple(data.values()) + tuple(conditions.values()))

    def delete(self, table, conditions):
        """
        Deletes rows from a specified table based on conditions.

        :param table: Name of the table.
        :param conditions: Dictionary of column-value pairs for filtering.
        """
        where_clause = " AND ".join([f"{col} = ?" for col in conditions.keys()])
        query = f"DELETE FROM {table} WHERE {where_clause}"
        self.execute(query, tuple(conditions.values()))
