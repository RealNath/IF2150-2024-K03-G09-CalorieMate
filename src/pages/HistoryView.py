# src/pages/HistoryView.py
import tkinter as tk
import sqlite3
from datetime import date
from config import COLOR_BACKGROUND, COLOR_TEXT
from tkinter import messagebox

class HistoryView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BACKGROUND)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        title_label = tk.Label(self, text="Histori Konsumsi", font=("Roboto", 18), bg=COLOR_BACKGROUND, fg=COLOR_TEXT)
        title_label.pack(pady=10)

        history_frame = tk.Frame(self, bg=COLOR_BACKGROUND)
        history_frame.pack(pady=10, padx=20)

        self.display_history(history_frame)

        clear_button = tk.Button(self, text="Hapus History", command=self.clear_history, font=("Comic Sans MS", 10), bg='red', fg='white')
        clear_button.pack(pady=20)

    def display_history(self, history_frame):
        conn = sqlite3.connect('src/database/database.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT date, plan_name, total_calories
            FROM UserPlan
            WHERE eaten = 1
            ORDER BY date DESC
        ''')
        eaten_plans = cursor.fetchall()

        for plan in eaten_plans:
            date_str, plan_name, total_calories = plan
            entry_text = f"{date_str} | {plan_name} | {total_calories} kcal"
            entry_label = tk.Label(history_frame, text=entry_text, font=("Verdana", 14), bg='light yellow', fg='black')
            entry_label.pack(anchor='w', pady=5)

        conn.close()

    def clear_history(self):
        conn = sqlite3.connect('src/database/database.db')
        cursor = conn.cursor()

        cursor.execute('''
            DELETE FROM UserPlan
            WHERE eaten = 1
        ''')

        conn.commit()
        conn.close()

        for widget in self.winfo_children():
            widget.destroy()
        self.create_widgets()
        print("History berhasil dihapus.")
