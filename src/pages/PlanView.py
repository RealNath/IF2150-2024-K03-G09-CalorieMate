# src/pages/PlanView.py
import tkinter as tk
from tkinter import ttk, messagebox
from logic.DatabaseManager import DatabaseManager
from datetime import date

Database = 'src/database/database.db'  # Path to database
db = DatabaseManager(Database)

class PlanView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.selected_date = date.today().isoformat()
        self.selected_foods = []  # List to store selected foods
        self.calorie_calculator = controller.calorie_calculator  # Access calorie calculator from controller
        self.create_widgets()

    def create_widgets(self):
        # Title Label
        title_label = ttk.Label(self, text="Your Plan", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        # Frame for plan details
        plan_frame = ttk.Frame(self)
        plan_frame.pack(pady=10, padx=20, fill="x")

        # Plan Name
        plan_name_label = ttk.Label(plan_frame, text="Plan Name:", font=("Arial", 12))
        plan_name_label.grid(row=0, column=0, sticky="w", pady=5)
        self.plan_name_entry = ttk.Entry(plan_frame, width=30)
        self.plan_name_entry.grid(row=0, column=1, pady=5, padx=10)

        # Meal Type
        meal_type_label = ttk.Label(plan_frame, text="Meal Type:", font=("Arial", 12))
        meal_type_label.grid(row=1, column=0, sticky="w", pady=5)
        self.meal_type_var = tk.StringVar()
        self.meal_type_combobox = ttk.Combobox(plan_frame, textvariable=self.meal_type_var, state="readonly")
        self.meal_type_combobox['values'] = ["breakfast", "brunch", "lunch", "dinner", "snack", "dessert", "appetizer", "supper"]
        self.meal_type_combobox.current(0)
        self.meal_type_combobox.grid(row=1, column=1, pady=5, padx=10)

        # Selected Date (From Calendar)
        date_label = ttk.Label(plan_frame, text="Date:", font=("Arial", 12))
        date_label.grid(row=2, column=0, sticky="w", pady=5)
        self.date_entry = ttk.Entry(plan_frame, width=30)
        self.date_entry.grid(row=2, column=1, pady=5, padx=10)
        self.date_entry.insert(0, self.selected_date)
        self.date_entry.config(state='readonly')  # Read-only as date is selected from calendar

        # Listbox for selected foods
        foods_label = ttk.Label(self, text="Selected Foods:", font=("Arial", 12))
        foods_label.pack(pady=(20, 5))
        self.foods_listbox = tk.Listbox(self, width=50, height=10)
        self.foods_listbox.pack(pady=5)

        # Buttons Frame
        buttons_frame = ttk.Frame(self)
        buttons_frame.pack(pady=10)

        add_food_button = ttk.Button(buttons_frame, text="Add Food", command=self.add_food)
        add_food_button.grid(row=0, column=0, padx=5)

        remove_food_button = ttk.Button(buttons_frame, text="Remove Selected Food", command=self.remove_selected_food)
        remove_food_button.grid(row=0, column=1, padx=5)

        # Save Plan Button
        save_plan_button = ttk.Button(self, text="Save Plan", command=self.save_plan)
        save_plan_button.pack(pady=20)

        # Load existing plan for selected date
        self.load_plan()

    def load_plan(self):
        # Fetch plans for the selected date
        db.connect()
        plans = db.read("UserPlan", ["plan_name, meal_type, total_calories"], {"date": self.selected_date}, False)
        db.disconnect()

        if plans:
            for plan in plans:
                plan_name, meal_type, total_calories = plan
                self.plan_name_entry.insert(0, plan_name)
                self.meal_type_var.set(meal_type)
                # Load foods into listbox
                self.load_foods_from_plan(plan_name)
        else:
            # No plan for the selected date
            pass

    def load_foods_from_plan(self, plan_name):
        db.connect()
        plan = db.read("PlanDatabase", ["food_items"], {"plan_name": plan_name}, True)
        db.disconnect()

        if plan:
            food_items = eval(plan[0])  # Convert string to list
            self.selected_foods = food_items
            self.update_foods_listbox()
        else:
            messagebox.showerror("Error", "Failed to load foods from the plan.")

    def add_food(self):
        # Open a new window to select food from FoodDatabase
        AddFoodPopup(self)

    def remove_selected_food(self):
        selected_indices = self.foods_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Selection Error", "No food item selected to remove.")
            return
        for index in reversed(selected_indices):
            food = self.foods_listbox.get(index)
            self.selected_foods.remove(food)
            self.foods_listbox.delete(index)

    def update_foods_listbox(self):
        self.foods_listbox.delete(0, tk.END)
        for food in self.selected_foods:
            self.foods_listbox.insert(tk.END, food)

    def save_plan(self):
        plan_name = self.plan_name_entry.get().strip()
        meal_type = self.meal_type_var.get()
        date_selected = self.date_entry.get()

        if not plan_name:
            messagebox.showwarning("Input Error", "Plan name cannot be empty.")
            return

        if not self.selected_foods:
            messagebox.showwarning("Input Error", "Please add at least one food item to the plan.")
            return

        # Calculate total calories
        total_calories = self.calorie_calculator.calculate_total_calories_for_foods(self.selected_foods)

        # Save to PlanDatabase
        db.connect()
        db.create("PlanDatabase", {
            "plan_name": plan_name,
            "meal_type": meal_type,
            "food_items": str(self.selected_foods),
            "total_calories": total_calories
        })
        db.disconnect()

        # Save to UserPlan
        db.connect()
        db.create("UserPlan", {
            "plan_name": plan_name,
            "date": date_selected,
            "meal_type": meal_type,
            "total_calories": total_calories,
            "eaten": False
        })
        db.disconnect()

        messagebox.showinfo("Success", "Plan saved successfully.")
        self.controller.show_page("PlanView")

class AddFoodPopup(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Add Food")
        self.geometry("300x400")
        self.parent = parent
        self.selected_food = None
        self.create_widgets()

    def create_widgets(self):
        # Label
        label = ttk.Label(self, text="Select Food to Add", font=("Arial", 14, "bold"))
        label.pack(pady=10)

        # Listbox for foods
        self.food_listbox = tk.Listbox(self, width=40, height=15)
        self.food_listbox.pack(pady=10, padx=10, fill="both", expand=True)

        # Scrollbar for listbox
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.food_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.food_listbox.config(yscrollcommand=scrollbar.set)

        # Load foods
        self.load_foods()

        # Add Button
        add_button = ttk.Button(self, text="Add Selected Food", command=self.add_selected_food)
        add_button.pack(pady=10)

    def load_foods(self):
        db.connect()
        foods = db.read("FoodDatabase", ["name"], None, False)
        db.disconnect()

        self.food_list = [food[0] for food in foods]
        for food in self.food_list:
            self.food_listbox.insert(tk.END, food)

    def add_selected_food(self):
        selection = self.food_listbox.curselection()
        if selection:
            index = selection[0]
            food_name = self.food_list[index]
            self.parent.selected_foods.append(food_name)
            self.parent.update_foods_listbox()
            self.destroy()
        else:
            messagebox.showwarning("Selection Error", "No food item selected.")
