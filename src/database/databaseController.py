# src/database/databaseController.py
import sqlite3

class DatabaseController:
    def __init__(self, db_path='src/database/database.db'):
        self.db_path = db_path
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def close(self):
        if self.conn:
            self.conn.commit()
            self.conn.close()
            self.conn = None
            self.cursor = None

    def read(self, table, columns=["*"], conditions=None, single=False):
        # columns: list of columns, conditions: dict of {col: val}, single: return one or all
        col_str = ", ".join(columns)
        sql = f"SELECT {col_str} FROM {table}"
        params = []
        if conditions:
            where_clause = " AND ".join([f"{k}=?" for k in conditions.keys()])
            sql += f" WHERE {where_clause}"
            params = list(conditions.values())
        self.cursor.execute(sql, params)
        return self.cursor.fetchone() if single else self.cursor.fetchall()

    def create(self, table, data):
        # data: dict of {col: val}
        cols = ", ".join(data.keys())
        placeholders = ", ".join(["?" for _ in data.keys()])
        sql = f"INSERT INTO {table} ({cols}) VALUES ({placeholders})"
        self.cursor.execute(sql, list(data.values()))

    def update(self, table, data, conditions):
        # data: dict of cols to update, conditions: dict for WHERE
        set_clause = ", ".join([f"{k}=?" for k in data.keys()])
        where_clause = " AND ".join([f"{k}=?" for k in conditions.keys()])
        sql = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        params = list(data.values()) + list(conditions.values())
        self.cursor.execute(sql, params)

    def delete(self, table, conditions):
        where_clause = " AND ".join([f"{k}=?" for k in conditions.keys()])
        sql = f"DELETE FROM {table} WHERE {where_clause}"
        self.cursor.execute(sql, list(conditions.values()))
