# src/pages/PlanView.py
import tkinter as tk
from tkinter import ttk, messagebox
from logic.DatabaseManager import DatabaseManager
from datetime import date
from config import COLOR_BACKGROUND, COLOR_TEXT

Database = 'src/database/database.db'  # Path to database
db = DatabaseManager(Database)

class PlanView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BACKGROUND)
        self.controller = controller
        self.selected_date = date.today().isoformat()
        self.calorie_calculator = controller.calorie_calculator
        self.create_widgets()

    def create_widgets(self):
        # Title Label
        title_label = ttk.Label(
            self,
            text="Your Plans",
            font=("Arial", 16, "bold"),
            foreground=COLOR_TEXT,
            background=COLOR_BACKGROUND
        )
        title_label.pack(pady=10)

        # Frame for plan list and add button
        plan_frame = ttk.Frame(self, style='MainContent.TFrame')
        plan_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Treeview to display plans
        columns = ("plan_id", "plan_name", "meal_type", "total_calories", "eaten")
        self.tree = ttk.Treeview(plan_frame, columns=columns, show='headings', selectmode='browse')
        self.tree.pack(side="left", fill="both", expand=True)

        # Define headings
        self.tree.heading("plan_id", text="ID")
        self.tree.heading("plan_name", text="Plan Name")
        self.tree.heading("meal_type", text="Meal Type")
        self.tree.heading("total_calories", text="Total Calories")
        self.tree.heading("eaten", text="Eaten")

        # Define column widths
        self.tree.column("plan_id", width=50, anchor='center')
        self.tree.column("plan_name", width=200, anchor='center')
        self.tree.column("meal_type", width=100, anchor='center')
        self.tree.column("total_calories", width=120, anchor='center')
        self.tree.column("eaten", width=80, anchor='center')

        # Bind double-click on Treeview
        self.tree.bind('<Double-1>', self.on_double_click)

        # Scrollbar for Treeview
        scrollbar = ttk.Scrollbar(plan_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="left", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Add Plan Button
        add_plan_button = ttk.Button(self, text="Add New Plan", command=self.open_add_plan_popup)
        add_plan_button.pack(pady=20)

        # Load existing plans
        self.load_plans()

    def load_plans(self):
        self.tree.delete(*self.tree.get_children())  # Clear existing entries
        db.connect()
        plans = db.read(
            "UserPlan",
            ["plan_id", "plan_name", "meal_type", "total_calories", "eaten"],
            {"date": self.selected_date},
            False
        )
        db.disconnect()

        self.plans = plans  # Store for reference

        for plan in plans:
            plan_id, plan_name, meal_type, total_calories, eaten = plan
            eaten_status = "Yes" if eaten else "No"
            self.tree.insert("", tk.END, values=(plan_id, plan_name, meal_type, total_calories, eaten_status))

    def on_double_click(self, event):
        item = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)
        if not item or not column:
            return

        # 'eaten' column is the 5th column (index '#5')
        if column == '#5':
            self.toggle_eaten_status(item)
        else:
            self.show_plan_details(item)

    def toggle_eaten_status(self, item):
        current_eaten = self.tree.set(item, "eaten")
        new_eaten = 0 if current_eaten == "Yes" else 1

        # Update the database
        plan_id = self.tree.set(item, "plan_id")
        db.connect()
        db.update("UserPlan", {"eaten": new_eaten}, {"plan_id": plan_id})
        db.disconnect()

        # Update the Treeview
        self.tree.set(item, "eaten", "Yes" if new_eaten else "No")

    def show_plan_details(self, item):
        plan_id = self.tree.set(item, "plan_id")
        plan_name = self.tree.set(item, "plan_name")

        # Fetch foods from the plan
        db.connect()
        plan = db.read("PlanDatabase", ["food_items"], {"plan_name": plan_name}, True)
        db.disconnect()

        if plan and plan[0][0]:
            food_items_str = plan[0][0]  # Assuming it's stored as a string representation of list
            food_items = eval(food_items_str)  # Convert string to list safely
        else:
            food_items = []

        # Fetch calories for each food
        food_details = []
        db.connect()
        for food in food_items:
            food_data = db.read("FoodDatabase", ["calories"], {"name": food}, True)
            if food_data:
                food_details.append((food, food_data[0][0]))
            else:
                food_details.append((food, "N/A"))
        db.disconnect()

        # Create a new window to display details
        details_window = tk.Toplevel(self)
        details_window.title(f"Details of {plan_name}")
        details_window.geometry("400x400")
        details_window.configure(bg=COLOR_BACKGROUND)

        # Title Label
        title_label = ttk.Label(
            details_window,
            text=f"Plan: {plan_name}",
            font=("Arial", 16, "bold"),
            foreground=COLOR_TEXT,
            background=COLOR_BACKGROUND
        )
        title_label.pack(pady=10)

        # Treeview for food details
        food_columns = ("food_name", "calories")
        food_tree = ttk.Treeview(details_window, columns=food_columns, show='headings')
        food_tree.pack(pady=10, padx=10, fill="both", expand=True)

        # Define headings
        food_tree.heading("food_name", text="Food Name")
        food_tree.heading("calories", text="Calories")

        # Define column widths
        food_tree.column("food_name", width=200, anchor='center')
        food_tree.column("calories", width=100, anchor='center')

        # Insert food items
        for food, calories in food_details:
            food_tree.insert("", tk.END, values=(food, calories))

        # Close Button
        close_button = ttk.Button(details_window, text="Close", command=details_window.destroy)
        close_button.pack(pady=10)

    def open_add_plan_popup(self):
        AddPlanPopup(self)

# src/pages/PlanView.py (continued)

class AddPlanPopup(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Add New Plan")
        self.geometry("400x500")
        self.configure(bg=COLOR_BACKGROUND)
        self.parent = parent
        self.selected_foods = []
        self.create_widgets()

    def create_widgets(self):
        # Title Label
        title_label = ttk.Label(
            self,
            text="Add New Plan",
            font=("Arial", 16, "bold"),
            foreground=COLOR_TEXT,
            background=COLOR_BACKGROUND
        )
        title_label.pack(pady=10)

        # Plan Name Entry
        plan_name_label = ttk.Label(
            self,
            text="Plan Name:",
            font=("Arial", 12),
            foreground=COLOR_TEXT,
            background=COLOR_BACKGROUND
        )
        plan_name_label.pack(pady=(10, 5), padx=20, anchor='w')
        self.plan_name_entry = ttk.Entry(self, width=40)
        self.plan_name_entry.pack(pady=5, padx=20)

        # Meal Type Dropdown
        meal_type_label = ttk.Label(
            self,
            text="Meal Type:",
            font=("Arial", 12),
            foreground=COLOR_TEXT,
            background=COLOR_BACKGROUND
        )
        meal_type_label.pack(pady=(10, 5), padx=20, anchor='w')
        self.meal_type_var = tk.StringVar()
        self.meal_type_combobox = ttk.Combobox(
            self,
            textvariable=self.meal_type_var,
            state="readonly"
        )
        self.meal_type_combobox['values'] = ["breakfast", "brunch", "lunch", "dinner", "snack", "dessert", "appetizer", "supper"]
        self.meal_type_combobox.current(0)
        self.meal_type_combobox.pack(pady=5, padx=20)

        # Food Selection Listbox
        food_label = ttk.Label(
            self,
            text="Select Foods:",
            font=("Arial", 12),
            foreground=COLOR_TEXT,
            background=COLOR_BACKGROUND
        )
        food_label.pack(pady=(10, 5), padx=20, anchor='w')
        self.food_listbox = tk.Listbox(
            self,
            selectmode='multiple',
            width=50,
            height=10
        )
        self.food_listbox.pack(pady=5, padx=20, fill="both", expand=True)

        # Load Foods from Database
        db.connect()
        foods = db.read("FoodDatabase", ["name"], None, False)
        db.disconnect()

        for food in foods:
            self.food_listbox.insert(tk.END, food[0])

        # Add and Remove Buttons
        buttons_frame = ttk.Frame(self, style='MainContent.TFrame')
        buttons_frame.pack(pady=10)

        add_food_button = ttk.Button(
            buttons_frame,
            text="Add Selected Foods",
            command=self.add_selected_foods
        )
        add_food_button.pack(side="left", padx=5)

        remove_food_button = ttk.Button(
            buttons_frame,
            text="Remove Selected Foods",
            command=self.remove_selected_foods
        )
        remove_food_button.pack(side="left", padx=5)

        # Selected Foods Listbox
        selected_food_label = ttk.Label(
            self,
            text="Selected Foods:",
            font=("Arial", 12),
            foreground=COLOR_TEXT,
            background=COLOR_BACKGROUND
        )
        selected_food_label.pack(pady=(10, 5), padx=20, anchor='w')
        self.selected_food_listbox = tk.Listbox(
            self,
            width=50,
            height=5
        )
        self.selected_food_listbox.pack(pady=5, padx=20, fill="both", expand=True)

        # Save Button
        save_button = ttk.Button(self, text="Save Plan", command=self.save_plan)
        save_button.pack(pady=20)

    def add_selected_foods(self):
        selected_indices = self.food_listbox.curselection()
        for index in selected_indices:
            food = self.food_listbox.get(index)
            if food not in self.selected_foods:
                self.selected_foods.append(food)
                self.selected_food_listbox.insert(tk.END, food)

    def remove_selected_foods(self):
        selected_indices = self.selected_food_listbox.curselection()
        for index in reversed(selected_indices):
            self.selected_foods.remove(self.selected_food_listbox.get(index))
            self.selected_food_listbox.delete(index)

    def save_plan(self):
        plan_name = self.plan_name_entry.get().strip()
        meal_type = self.meal_type_var.get()
        selected_date = self.parent.selected_date

        if not plan_name:
            messagebox.showwarning("Input Error", "Plan name cannot be empty.")
            return

        if not self.selected_foods:
            messagebox.showwarning("Input Error", "Please select at least one food item.")
            return

        # Calculate total calories
        total_calories = self.parent.calorie_calculator.calculate_total_calories_for_foods(self.selected_foods)

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
            "date": selected_date,
            "meal_type": meal_type,
            "total_calories": total_calories,
            "eaten": False
        })
        db.disconnect()

        messagebox.showinfo("Success", "Plan saved successfully.")
        self.parent.load_plans()
        self.destroy()
