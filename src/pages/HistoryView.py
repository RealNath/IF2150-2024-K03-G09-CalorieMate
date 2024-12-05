import tkinter as tk
import sqlite3
from datetime import date

class HistoryView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller 
        self.create_widgets()

    def create_widgets(self):
        # Back button
        back_button = tk.Button(self, text="Back", command=lambda: self.controller.show_page("MainApp"))
        back_button.pack(anchor='ne', padx=10, pady=10)

        title_label = tk.Label(self, text="Histori Konsumsi", font=("Arial", 18))
        title_label.pack(pady=10)

        history_frame = tk.Frame(self)
        history_frame.pack(pady=10, padx=20)

        self.display_history(history_frame)

        # Clear History Button
        clear_button = tk.Button(self, text="Hapus History", command=self.clear_history)
        clear_button.pack(pady=20)

    def display_history(self, history_frame):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Get history of all eaten plans sorted by date (descending)
        cursor.execute('''
            SELECT date, plan_name, total_calories
            FROM UserPlan
            WHERE eaten = 1
            ORDER BY date DESC
        ''')
        eaten_plans = cursor.fetchall()

        # Display each eaten plan in the Table
        for plan in eaten_plans:
            date_str, plan_name, total_calories = plan
            entry_text = f"{date_str} | {plan_name} | {total_calories} kcal"
            entry_label = tk.Label(history_frame, text=entry_text, font=("Arial", 14))
            entry_label.pack(anchor='w', pady=5)

        conn.close()

    def clear_history(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Delete 'eaten'
        cursor.execute('''
            DELETE FROM UserPlan
            WHERE eaten = 1
        ''')

        conn.commit()
        conn.close()

        # Clear the history
        for widget in self.winfo_children():
            widget.destroy()
        self.create_widgets()
        print("History berhasil dihapus.")
