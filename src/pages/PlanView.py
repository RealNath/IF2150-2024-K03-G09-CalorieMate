import tkinter as tk
import sqlite3
from datetime import date

class PlanView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        today = date.today().isoformat()

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute("SELECT plan_name, meal_type FROM UserPlan WHERE date = ?", (today,))
        plans = cursor.fetchall()

        if plans:
            for plan in plans:
                plan_label = tk.Label(self, text=f"Plan: {plan[0]}, Meal Type: {plan[1]}")
                plan_label.pack()
        else:
            no_plan_label = tk.Label(self, text="No plans for today.")
            no_plan_label.pack()

            # 'Make a Plan' Button
            make_plan_button = tk.Button(self, text="Make a Plan", command=lambda: self.controller.show_page("MakePlanView"))
            make_plan_button.pack(pady=10)

        # 'Add a Plan' Button
        add_plan_button = tk.Button(self, text="Add a Plan", command=self.add_plan)
        add_plan_button.pack(pady=10)

        conn.close()

    def add_plan(self):
        # This use placeholder plan information (to be replaced by user input)
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        today = date.today().isoformat()
        plan_name = "your_plan_name"
        meal_type = "meal_type"
        cursor.execute("INSERT INTO UserPlan (plan_name, date, meal_type, total_calories, eaten) VALUES (?, ?, ?, ?, ?)", (plan_name, today, meal_type, 600, False))
        
        conn.commit()
        conn.close()
