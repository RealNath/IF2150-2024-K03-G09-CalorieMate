# src/pages/HistoryView.py
import tkinter as tk
import sqlite3
from datetime import date
from config import COLOR_BACKGROUND, COLOR_TEXT  # Updated import
from tkinter import ttk, messagebox

class HistoryView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BACKGROUND)  # Use COLOR_BACKGROUND from config
        self.controller = controller 
        self.create_widgets()

    def create_widgets(self):
        # Back button
        back_button = tk.Button(self, text="Back", command=lambda: self.controller.show_page("MainApp"))
        back_button.pack(anchor='ne', padx=10, pady=10)

        title_label = tk.Label(self, text="Histori Konsumsi", font=("Arial", 18), bg=COLOR_BACKGROUND, fg=COLOR_TEXT)
        title_label.pack(pady=10)

        history_frame = tk.Frame(self, bg=COLOR_BACKGROUND)
        history_frame.pack(pady=10, padx=20)

        self.display_history(history_frame)

        # Clear History Button
        clear_button = tk.Button(self, text="Hapus History", command=self.clear_history)
        clear_button.pack(pady=20)

    def refresh_data(self):
        for w in self.history_frame.winfo_children():
            w.destroy()

        self.db_controller.connect()
        eaten_plans = self.db_controller.read("UserPlan", ["date","plan_name","total_calories"], {"eaten":1}, False)
        self.db_controller.close()

        if not eaten_plans:
            no_label = ttk.Label(self.history_frame, text="No eaten plans history.", style='MainContent.TLabel')
            no_label.pack(pady=10, padx=10)
        else:
            # Sort by date descending if needed manually
            eaten_plans_sorted = sorted(eaten_plans, key=lambda x: x[0], reverse=True)
            for plan in eaten_plans_sorted:
                date_str, plan_name, total_cal = plan
                entry = f"{date_str} | {plan_name} | {total_cal} kcal"
                lbl = ttk.Label(self.history_frame, text=entry, background=COLOR_BACKGROUND)
                lbl.pack(anchor='w', pady=5)

    def clear_history(self):
        confirm = messagebox.askyesno("Confirm", "Clear history?")
        if confirm:
            self.db_controller.connect()
            self.db_controller.cursor.execute("DELETE FROM UserPlan WHERE eaten=1")
            self.db_controller.close()
            self.refresh_data()
