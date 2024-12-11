# src/logic/DatabaseManager.py
import sqlite3

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def disconnect(self):
        self.conn.commit()
        self.conn.close()

    def create(self, table, data):
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        values = tuple(data.values())
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        self.cursor.execute(query, values)

    def read(self, table, columns, conditions=None, single=False):
        cols = ', '.join(columns)
        query = f"SELECT {cols} FROM {table}"
        values = []
        if conditions:
            conds = ' AND '.join([f"{k} = ?" for k in conditions.keys()])
            query += f" WHERE {conds}"
            values = list(conditions.values())
        self.cursor.execute(query, values)
        if single:
            return self.cursor.fetchone()
        else:
            return self.cursor.fetchall()

    def update(self, table, data, conditions):
        set_clause = ', '.join([f"{k} = ?" for k in data.keys()])
        cond_clause = ' AND '.join([f"{k} = ?" for k in conditions.keys()])
        values = list(data.values()) + list(conditions.values())
        query = f"UPDATE {table} SET {set_clause} WHERE {cond_clause}"
        self.cursor.execute(query, values)

    def delete(self, table, conditions):
        cond_clause = ' AND '.join([f"{k} = ?" for k in conditions.keys()])
        values = list(conditions.values())
        query = f"DELETE FROM {table} WHERE {cond_clause}"
        self.cursor.execute(query, values)
