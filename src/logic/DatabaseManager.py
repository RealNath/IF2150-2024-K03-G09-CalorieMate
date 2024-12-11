# src/logic/DatabaseManager.py
import sqlite3
import json

class DatabaseManager:
    def __init__(self, db_path='src/database/database.db'):
        self.db_path = db_path
        self.conn = None
        self.cursor = None

    def connect(self):
        if not self.conn:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            self.cursor.execute("PRAGMA foreign_keys = ON;")

    def disconnect(self):
        if self.conn:
            self.conn.commit()
            self.conn.close()
            self.conn = None
            self.cursor = None

    def read(self, table, columns=["*"], conditions=None, single=False):
        col_str = ", ".join(columns)
        sql = f"SELECT {col_str} FROM {table}"
        params = []
        if conditions:
            conds = " AND ".join([f"{k}=?" for k in conditions.keys()])
            sql += f" WHERE {conds}"
            params = list(conditions.values())
        self.cursor.execute(sql, params)
        if single:
            return self.cursor.fetchone()
        else:
            return self.cursor.fetchall()

    def create(self, table, data):
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data))
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        self.cursor.execute(sql, list(data.values()))

    def update(self, table, data, conditions):
        set_clause = ", ".join([f"{k}=?" for k in data.keys()])
        cond_clause = " AND ".join([f"{k}=?" for k in conditions.keys()])
        params = list(data.values()) + list(conditions.values())
        sql = f"UPDATE {table} SET {set_clause} WHERE {cond_clause}"
        self.cursor.execute(sql, params)

    def delete(self, table, conditions):
        cond_clause = " AND ".join([f"{k}=?" for k in conditions.keys()])
        params = list(conditions.values())
        sql = f"DELETE FROM {table} WHERE {cond_clause}"
        self.cursor.execute(sql, params)
