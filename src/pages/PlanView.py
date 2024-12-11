# src/pages/PlanView.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from config import COLOR_BACKGROUND, COLOR_TEXT
import json

class PlanView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BACKGROUND)
        self.controller = controller
        self.selected_date = date.today().isoformat()
        self.calorie_calculator = controller.calorie_calculator
        self.create_widgets()

    def create_widgets(self):
        title_label = ttk.Label(
            self,
            text="Your Plans",
            font=("Arial", 16, "bold"),
            foreground=COLOR_TEXT,
            background=COLOR_BACKGROUND
        )
        title_label.pack(pady=10)

        plan_frame = ttk.Frame(self, style='MainContent.TFrame')
        plan_frame.pack(pady=10, padx=20, fill="both", expand=True)

        columns = ("plan_id", "plan_name", "meal_type", "total_calories", "eaten")
        self.tree = ttk.Treeview(plan_frame, columns=columns, show='headings', selectmode='browse')
        self.tree.pack(side="left", fill="both", expand=True)

        self.tree.heading("plan_id", text="ID")
        self.tree.heading("plan_name", text="Plan Name")
        self.tree.heading("meal_type", text="Meal Type")
        self.tree.heading("total_calories", text="Total Calories")
        self.tree.heading("eaten", text="Eaten")

        self.tree.column("plan_id", width=50, anchor='center')
        self.tree.column("plan_name", width=200, anchor='center')
        self.tree.column("meal_type", width=100, anchor='center')
        self.tree.column("total_calories", width=120, anchor='center')
        self.tree.column("eaten", width=80, anchor='center')

        self.tree.bind('<Double-1>', self.on_double_click)

        scrollbar = ttk.Scrollbar(plan_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="left", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        add_plan_button = ttk.Button(self, text="Add New Plan", command=lambda: self.controller.show_page("MakePlanView"))
        add_plan_button.pack(pady=20)

        self.load_plans()

    def load_plans(self):
        self.tree.delete(*self.tree.get_children())
        self.controller.db_manager.connect()
        plans = self.controller.db_manager.read(
            table="UserPlan",
            columns=["plan_id", "plan_name", "meal_type", "total_calories", "eaten"],
            conditions={"date": self.selected_date},
            single=False
        )
        self.controller.db_manager.disconnect()

        self.plans = plans
        for plan in plans:
            plan_id, plan_name, meal_type, total_calories, eaten = plan
            eaten_status = "Yes" if eaten else "No"
            self.tree.insert("", tk.END, values=(plan_id, plan_name, meal_type, total_calories, eaten_status))

    def on_double_click(self, event):
        item = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)
        if not item or not column:
            return

        if column == '#5':
            self.toggle_eaten_status(item)
        else:
            self.show_plan_details(item)

    def toggle_eaten_status(self, item):
        current_eaten = self.tree.set(item, "eaten")
        new_eaten = 0 if current_eaten == "Yes" else 1

        plan_id = int(self.tree.set(item, "plan_id"))
        self.controller.db_manager.connect()
        self.controller.db_manager.update(
            table="UserPlan",
            data={"eaten": new_eaten},
            conditions={"plan_id": plan_id, "date": self.selected_date}
        )
        self.controller.db_manager.disconnect()

        self.tree.set(item, "eaten", "Yes" if new_eaten else "No")

    def show_plan_details(self, item):
        plan_id = int(self.tree.set(item, "plan_id"))
        plan_name = self.tree.set(item, "plan_name")

        self.controller.db_manager.connect()
        plan = self.controller.db_manager.read(
            table="PlanDatabase",
            columns=["food_items"],
            conditions={"plan_id": plan_id, "plan_name": plan_name},
            single=True
        )
        self.controller.db_manager.disconnect()

        if plan:
            try:
                food_items = json.loads(plan[0])
            except:
                food_items = eval(plan[0])
        else:
            food_items = []

        if not food_items:
            messagebox.showinfo("No Foods", "This plan has no associated food items.")
            return

        food_details = []
        self.controller.db_manager.connect()
        for food in food_items:
            food_data = self.controller.db_manager.read(
                table="FoodDatabase",
                columns=["calories"],
                conditions={"name": food},
                single=True
            )
            if food_data and food_data[0]:
                food_details.append((food, food_data[0]))
            else:
                food_details.append((food, "N/A"))
        self.controller.db_manager.disconnect()

        details_window = tk.Toplevel(self)
        details_window.title(f"Details of {plan_name}")
        details_window.geometry("400x400")
        details_window.configure(bg=COLOR_BACKGROUND)

        title_label = ttk.Label(
            details_window,
            text=f"Plan: {plan_name}",
            font=("Arial", 16, "bold"),
            foreground=COLOR_TEXT,
            background=COLOR_BACKGROUND
        )
        title_label.pack(pady=10)

        food_columns = ("food_name", "calories")
        food_tree = ttk.Treeview(details_window, columns=food_columns, show='headings')
        food_tree.pack(pady=10, padx=10, fill="both", expand=True)

        food_tree.heading("food_name", text="Food Name")
        food_tree.heading("calories", text="Calories")

        food_tree.column("food_name", width=200, anchor='center')
        food_tree.column("calories", width=100, anchor='center')

        for food, calories in food_details:
            food_tree.insert("", tk.END, values=(food, calories))

        close_button = ttk.Button(details_window, text="Close", command=details_window.destroy)
        close_button.pack(pady=10)
