# src/pages/MakePlanView.py
import tkinter as tk
from tkinter import ttk, messagebox
from config import COLOR_BACKGROUND, COLOR_TEXT
from datetime import datetime
import json

class MakePlanView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BACKGROUND)
        self.controller = controller
        self.calorie_calculator = controller.calorie_calculator
        self.food_quantities = {}
        self.create_widgets()

    def create_widgets(self):
        notebook = ttk.Notebook(self)
        notebook.pack(pady=10, padx=10, fill="both", expand=True)

        self.add_existing_plan_tab = ttk.Frame(notebook, style='MainContent.TFrame')
        self.create_new_plan_tab = ttk.Frame(notebook, style='MainContent.TFrame')

        notebook.add(self.add_existing_plan_tab, text='Add Existing Plan')
        notebook.add(self.create_new_plan_tab, text='Create New Plan')

        self.setup_add_existing_plan_tab()
        self.setup_create_new_plan_tab()

    def setup_add_existing_plan_tab(self):
        tab = self.add_existing_plan_tab
        plan_label = ttk.Label(tab, text="Select an Existing Plan:", font=("Arial", 12, "bold"),
                               foreground=COLOR_TEXT, background=COLOR_BACKGROUND)
        plan_label.pack(pady=10, padx=10, anchor='w')

        self.existing_plans_var = tk.StringVar()
        self.existing_plans_combobox = ttk.Combobox(tab, textvariable=self.existing_plans_var, state="readonly", width=50)
        self.existing_plans_combobox.pack(pady=5, padx=10)
        self.load_existing_plans()

        date_label = ttk.Label(tab, text="Select Date:", font=("Arial", 12, "bold"),
                               foreground=COLOR_TEXT, background=COLOR_BACKGROUND)
        date_label.pack(pady=(20, 10), padx=10, anchor='w')

        self.date_entry = ttk.Entry(tab, width=20)
        self.date_entry.pack(pady=5, padx=10)

        instructions = ttk.Label(tab, text="Enter date in YYYY-MM-DD format.",
                                 foreground=COLOR_TEXT, background=COLOR_BACKGROUND)
        instructions.pack(pady=5, padx=10, anchor='w')

        add_plan_button = ttk.Button(tab, text="Add Plan to Selected Date",
                                     command=self.add_existing_plan_to_userplan)
        add_plan_button.pack(pady=20)

    def load_existing_plans(self):
        self.controller.db_manager.connect()
        plans = self.controller.db_manager.read("PlanDatabase", ["plan_id", "plan_name"], None, False)
        self.controller.db_manager.disconnect()

        self.existing_plans = plans
        plan_names = [f"{p[1]} (ID: {p[0]})" for p in plans]
        self.existing_plans_combobox['values'] = plan_names
        if plan_names:
            self.existing_plans_combobox.current(0)

    def add_existing_plan_to_userplan(self):
        idx = self.existing_plans_combobox.current()
        if idx == -1:
            messagebox.showwarning("No Plan Selected", "Please select a plan to add.")
            return

        plan_id, plan_name = self.existing_plans[idx]
        selected_date = self.date_entry.get().strip()
        if not selected_date:
            messagebox.showwarning("No Date Entered", "Please enter a date in YYYY-MM-DD format.")
            return

        if not self.validate_date_format(selected_date):
            messagebox.showwarning("Invalid Date Format", "Please enter the date in YYYY-MM-DD format.")
            return

        self.controller.db_manager.connect()
        existing_entry = self.controller.db_manager.read("UserPlan", ["plan_id"], {"plan_id": plan_id, "date": selected_date}, True)
        self.controller.db_manager.disconnect()
        if existing_entry:
            messagebox.showwarning("Plan Already Exists", f"The plan '{plan_name}' is already added for {selected_date}.")
            return

        self.controller.db_manager.connect()
        plan_data = self.controller.db_manager.read("PlanDatabase", ["total_calories"], {"plan_id": plan_id}, True)
        self.controller.db_manager.disconnect()
        if not plan_data:
            messagebox.showerror("Error", "Selected plan does not exist in PlanDatabase.")
            return

        total_calories = plan_data[0]

        self.controller.db_manager.connect()
        meal_type_data = self.controller.db_manager.read("PlanDatabase", ["meal_type"], {"plan_id": plan_id}, True)
        self.controller.db_manager.disconnect()
        meal_type = meal_type_data[0] if meal_type_data else ""

        self.controller.db_manager.connect()
        self.controller.db_manager.create("UserPlan", {
            "plan_id": plan_id,
            "plan_name": plan_name,
            "date": selected_date,
            "meal_type": meal_type,
            "total_calories": total_calories,
            "eaten": False
        })
        self.controller.db_manager.disconnect()

        messagebox.showinfo("Success", f"Plan '{plan_name}' has been added to {selected_date}.")
        self.date_entry.delete(0, tk.END)

        # Refresh PlanView if currently visible
        if hasattr(self.controller.main_content, "current_page") and hasattr(self.controller.main_content.current_page, "load_plans"):
            self.controller.main_content.current_page.load_plans()

    def validate_date_format(self, date_str):
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def setup_create_new_plan_tab(self):
        tab = self.create_new_plan_tab
        plan_name_label = ttk.Label(tab, text="Enter New Plan Name:", font=("Arial", 12, "bold"),
                                    foreground=COLOR_TEXT, background=COLOR_BACKGROUND)
        plan_name_label.pack(pady=10, padx=10, anchor='w')

        self.new_plan_name_entry = ttk.Entry(tab, width=50)
        self.new_plan_name_entry.pack(pady=5, padx=10)

        meal_type_label = ttk.Label(tab, text="Select Meal Type:", font=("Arial", 12, "bold"),
                                    foreground=COLOR_TEXT, background=COLOR_BACKGROUND)
        meal_type_label.pack(pady=10, padx=10, anchor='w')

        self.new_meal_type_var = tk.StringVar()
        self.new_meal_type_combobox = ttk.Combobox(
            tab,
            textvariable=self.new_meal_type_var,
            state="readonly",
            width=47
        )
        self.new_meal_type_combobox['values'] = ["breakfast", "brunch", "lunch", "dinner", "snack",
                                                 "dessert", "appetizer", "supper"]
        self.new_meal_type_combobox.current(0)
        self.new_meal_type_combobox.pack(pady=5, padx=10)

        food_label = ttk.Label(tab, text="Select Foods for the Plan:", font=("Arial", 12, "bold"),
                               foreground=COLOR_TEXT, background=COLOR_BACKGROUND)
        food_label.pack(pady=10, padx=10, anchor='w')

        self.food_selection_frame = ttk.Frame(tab, style='MainContent.TFrame')
        self.food_selection_frame.pack(pady=5, padx=10, fill="both", expand=True)

        canvas = tk.Canvas(self.food_selection_frame, bg=COLOR_BACKGROUND)
        scrollbar = ttk.Scrollbar(self.food_selection_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='MainContent.TFrame')

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0,0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.controller.db_manager.connect()
        foods = self.controller.db_manager.read("FoodDatabase", ["name"], None, False)
        self.controller.db_manager.disconnect()

        self.food_widgets = {}
        for f in foods:
            food_name = f[0]
            self.food_quantities[food_name] = 0

            item_frame = ttk.Frame(scrollable_frame, style='MainContent.TFrame')
            item_frame.pack(fill="x", pady=2)

            name_label = ttk.Label(item_frame, text=food_name, font=("Arial", 12), foreground=COLOR_TEXT, background=COLOR_BACKGROUND)
            name_label.pack(side="left", padx=5)

            minus_button = ttk.Button(item_frame, text="-", width=3, command=lambda fn=food_name: self.decrement_food(fn))
            minus_button.pack(side="right", padx=5)

            quantity_label = ttk.Label(item_frame, text="0", width=5, font=("Arial", 12), foreground=COLOR_TEXT, background=COLOR_BACKGROUND)
            quantity_label.pack(side="right")

            plus_button = ttk.Button(item_frame, text="+", width=3, command=lambda fn=food_name: self.increment_food(fn))
            plus_button.pack(side="right", padx=5)

            self.food_widgets[food_name] = quantity_label

        self.total_calories_label = ttk.Label(tab, text="Total Calories: 0", font=("Arial", 12),
                                              foreground=COLOR_TEXT, background=COLOR_BACKGROUND)
        self.total_calories_label.pack(pady=10, padx=10, anchor='w')

        self.update_total_calories()

        add_new_plan_button = ttk.Button(tab, text="Create and Add New Plan", command=self.create_and_add_new_plan)
        add_new_plan_button.pack(pady=20)

    def increment_food(self, food_name):
        self.food_quantities[food_name] += 1
        self.food_widgets[food_name].config(text=str(self.food_quantities[food_name]))
        self.update_total_calories()

    def decrement_food(self, food_name):
        if self.food_quantities[food_name] > 0:
            self.food_quantities[food_name] -= 1
            self.food_widgets[food_name].config(text=str(self.food_quantities[food_name]))
            self.update_total_calories()

    def update_total_calories(self):
        total_calories = 0
        self.controller.db_manager.connect()
        for food, qty in self.food_quantities.items():
            food_data = self.controller.db_manager.read("FoodDatabase", ["calories"], {"name": food}, True)
            if food_data and food_data[0]:
                total_calories += food_data[0] * qty
        self.controller.db_manager.disconnect()

        self.total_calories_label.config(text=f"Total Calories: {total_calories}")

    def create_and_add_new_plan(self):
        plan_name = self.new_plan_name_entry.get().strip()
        if not plan_name:
            messagebox.showwarning("Input Error", "Please enter a plan name.")
            return

        meal_type = self.new_meal_type_var.get()

        selected_foods = []
        for food, qty in self.food_quantities.items():
            selected_foods.extend([food] * qty)

        if not selected_foods:
            messagebox.showwarning("Input Error", "Please select at least one food item.")
            return

        total_calories = self.calorie_calculator.calculate_total_calories_for_foods(selected_foods)

        self.controller.db_manager.connect()
        existing_plan = self.controller.db_manager.read("PlanDatabase", ["plan_id"], {"plan_name": plan_name}, True)
        if existing_plan:
            messagebox.showwarning("Duplicate Plan", "A plan with this name already exists.")
            self.controller.db_manager.disconnect()
            return

        self.controller.db_manager.create("PlanDatabase", {
            "plan_name": plan_name,
            "meal_type": meal_type,
            "food_items": json.dumps(selected_foods),
            "total_calories": total_calories
        })

        new_plan = self.controller.db_manager.read("PlanDatabase", ["plan_id"], {"plan_name": plan_name}, True)
        self.controller.db_manager.disconnect()

        if not new_plan:
            messagebox.showerror("Error", "Failed to retrieve the newly created plan.")
            return

        plan_id = new_plan[0]

        # Now we get the selected date from the controller directly
        selected_date = self.controller.selected_date
        if not selected_date:
            messagebox.showerror("Error", "No selected date is available.")
            return

        self.controller.db_manager.connect()
        existing_user_plan = self.controller.db_manager.read(
            "UserPlan", ["plan_id"], {"plan_id": plan_id, "date": selected_date}, True
        )
        self.controller.db_manager.disconnect()
        if existing_user_plan:
            messagebox.showwarning("Plan Already Exists", f"The plan '{plan_name}' is already added for {selected_date}.")
            return

        self.controller.db_manager.connect()
        self.controller.db_manager.create("UserPlan", {
            "plan_id": plan_id,
            "plan_name": plan_name,
            "date": selected_date,
            "meal_type": meal_type,
            "total_calories": total_calories,
            "eaten": False
        })
        self.controller.db_manager.disconnect()

        messagebox.showinfo("Success", f"New plan '{plan_name}' has been created and added to {selected_date}.")

        self.new_plan_name_entry.delete(0, tk.END)
        self.new_meal_type_combobox.current(0)
        for food in self.food_quantities:
            self.food_quantities[food] = 1
            self.food_widgets[food].config(text="1")
        self.update_total_calories()

        if hasattr(self.controller.main_content, "current_page") and hasattr(self.controller.main_content.current_page, "load_plans"):
            self.controller.main_content.current_page.load_plans()
