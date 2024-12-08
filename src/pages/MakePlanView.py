import tkinter as tk
import sqlite3
from logic.calorieCalculator import CalorieCalculator
from logic.DatabaseManager import DatabaseManager
from tkinter import messagebox  # To show confirmation messages

Database = 'src/database/database.db'  # Path to database
db = DatabaseManager(Database)

class MakePlanView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.selected_foods = []  # List to store selected foods
        self.food_labels = []  # List to store label references for displaying selected foods
        self.calorie_calculator = CalorieCalculator()
        self.create_widgets()

    def create_widgets(self):
        # Clear the frame to avoid adding widgets repeatedly
        for widget in self.winfo_children():
            widget.destroy()

        # 'Back to Plan View' Button
        back_button = tk.Button(self, text="Back to Plan View", command=lambda: self.controller.show_page("PlanView"))
        back_button.grid(row=0, column=0, columnspan=3, pady=10)

        # Input for Plan Name
        self.plan_name_label = tk.Label(self, text="Enter Plan Name:")
        self.plan_name_label.grid(row=1, column=0, pady=20, padx=10, sticky="w")

        self.plan_name_entry = tk.Entry(self)
        self.plan_name_entry.grid(row=1, column=1, pady=10, padx=10)

        # Dropdown for selecting the meal type
        self.meal_type_label = tk.Label(self, text="Select Meal Type:")
        self.meal_type_label.grid(row=2, column=0, pady=10, padx=10, sticky="w")

        self.meal_types = ["breakfast", "brunch", "lunch", "dinner", "snack", "dessert", "appetizer", "supper"]
        self.meal_type_var = tk.StringVar(self)
        self.meal_type_var.set(self.meal_types[0])  # Default value

        self.meal_type_menu = tk.OptionMenu(self, self.meal_type_var, *self.meal_types)
        self.meal_type_menu.grid(row=2, column=1, pady=10, padx=10)

        # List available foods from FoodDatabase
        db.connect()

        foods = db.read("FoodDatabase", ["name"], None, False)

        # Display each food and the + and - buttons side by side
        row = 3  # Start after the meal type dropdown
        for food in foods:
            food_name = food[0]
            food_label = tk.Label(self, text=food_name)
            food_label.grid(row=row, column=0, pady=5, padx=10, sticky="w")

            add_button = tk.Button(self, text="+", command=lambda name=food_name: self.add_food_to_plan(name))
            add_button.grid(row=row, column=1, pady=5, padx=10)

            remove_button = tk.Button(self, text="-", command=lambda name=food_name: self.remove_food_from_plan(name))
            remove_button.grid(row=row, column=2, pady=5, padx=10)

            row += 1  # Move to the next row for the next food item

        # Section to show the foods selected for the plan
        self.selected_foods_label = tk.Label(self, text="Selected Foods for Plan:")
        self.selected_foods_label.grid(row=row, column=0, pady=10, padx=10, sticky="w")

        self.selected_food_listbox = tk.Listbox(self)
        self.selected_food_listbox.grid(row=row + 1, column=0, columnspan=3, pady=10, padx=10)

        # 'Add Plan to Database' Button
        add_plan_button = tk.Button(self, text="Add Plan to Database", command=self.add_plan_to_database)
        add_plan_button.grid(row=row + 2, column=0, columnspan=3, pady=20)

        db.disconnect()

    def add_food_to_plan(self, food_name):
        self.selected_foods.append(food_name)
        self.update_selected_foods_listbox()
        print(f"Added {food_name} to the plan.")

    def remove_food_from_plan(self, food_name):
        if food_name in self.selected_foods:
            self.selected_foods.remove(food_name)
            self.update_selected_foods_listbox()
            print(f"Removed {food_name} from the plan.")
        else:
            print(f"{food_name} is not in the plan.")

    def update_selected_foods_listbox(self):
        """Update the Listbox with the selected foods"""
        self.selected_food_listbox.delete(0, tk.END)
        for food in self.selected_foods:
            self.selected_food_listbox.insert(tk.END, food)

    def add_plan_to_database(self):
        if not self.selected_foods:
            messagebox.showwarning("Empty Plan", "Please add some food items to the plan before saving.")
            return

        # Get the plan name from the input field
        plan_name = self.plan_name_entry.get().strip()

        if not plan_name:
            messagebox.showwarning("Empty Plan Name", "Please enter a name for the plan.")
            return

        # Get the selected meal type from the dropdown
        meal_type = self.meal_type_var.get()

        food_items = str(self.selected_foods)

        # Calculate total calories
        total_calories = self.calculate_total_calories()

        # Save the plan to PlanDatabase
        db.connect()

        db.create("PlanDatabase", {"plan_name" : plan_name, "meal_type" : meal_type, "food_items" : food_items, "total_calories" : total_calories})
        db.disconnect()
        print(f"Added {plan_name} to the PlanDatabase with total calories: {total_calories}")

        # Show confirmation message
        messagebox.showinfo("Plan Added", f"The plan '{plan_name}' has been added with a total of {total_calories} calories.")

        # Optionally, go back to the previous page (FoodView or another page)
        self.controller.show_page("PlanView")

    def calculate_total_calories(self):
        db.connect()

        total_calories = 0
        for food_name in self.selected_foods:
            food_data = db.read("FoodDatabase", ["calories"], {"name": food_name}, True)
            if food_data:
                total_calories += food_data[0]

        db.disconnect()
        return total_calories
