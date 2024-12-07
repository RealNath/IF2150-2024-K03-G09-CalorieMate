import tkinter as tk
import sqlite3
from logic.calorieCalculator import CalorieCalculator

Database = 'src/database/database.db' # Path to database

class MakePlanView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.selected_foods = []
        self.calorie_calculator = CalorieCalculator()
        self.create_widgets()

    def create_widgets(self):
        # List available foods from FoodDatabase
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM FoodDatabase")
        foods = cursor.fetchall()

        for food in foods:
            food_name = food[0]
            food_label = tk.Label(self, text=food_name)
            food_label.pack()

            add_button = tk.Button(self, text="+", command=lambda name=food_name: self.add_food_to_plan(name))
            add_button.pack()

        # 'Add Plan to Database' Button
        add_plan_button = tk.Button(self, text="Add Plan to Database", command=self.add_plan_to_database)
        add_plan_button.pack(pady=20)

        conn.close()

    def add_food_to_plan(self, food_name):
        self.selected_foods.append(food_name)
        print(f"Added {food_name} to the plan.")

    def add_plan_to_database(self):
        # Placeholder plan details
        plan_name = "custom_plan"
        meal_type = "lunch"
        food_items = str(self.selected_foods)

        # Calculate total calories
        total_calories = self.calculate_total_calories()

        # Save the plan to PlanDatabase
        conn = sqlite3.connect(Database)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO PlanDatabase (plan_name, meal_type, food_items, total_calories) VALUES (?, ?, ?, ?)",
                       (plan_name, meal_type, food_items, total_calories))
        conn.commit()
        conn.close()
        print(f"Added {plan_name} to the PlanDatabase with total calories: {total_calories}")

    def calculate_total_calories(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        total_calories = 0
        for food_name in self.selected_foods:
            cursor.execute('''
                SELECT calories
                FROM FoodDatabase
                WHERE name = ?
            ''', (food_name,))
            food_data = cursor.fetchone()
            if food_data:
                total_calories += food_data[0]

        conn.close()
        return total_calories
    