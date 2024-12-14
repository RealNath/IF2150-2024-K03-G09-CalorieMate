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
        self.selected_date = controller.selected_date
        self.calorie_calculator = controller.calorie_calculator
        self.create_widgets()

    def create_widgets(self):
        # Create a Notebook to separate "User Plans" and "All Plans"
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, pady=10, padx=10)

        # ---------------------------
        # User Plans Tab
        # ---------------------------
        self.user_plans_tab = ttk.Frame(self.notebook, style='MainContent.TFrame')
        self.notebook.add(self.user_plans_tab, text="User Plans")

        title_label = ttk.Label(
            self.user_plans_tab,
            text="Your Plans",
            font=("Roboto", 16, "bold"),
            foreground=COLOR_TEXT,
            background=COLOR_BACKGROUND
        )
        title_label.pack(pady=10)

        plan_frame = ttk.Frame(self.user_plans_tab, style='MainContent.TFrame')
        plan_frame.pack(pady=10, padx=20, fill="both", expand=True)

        columns = ("plan_id", "plan_name", "meal_type", "total_calories", "eaten")
        self.user_plan_tree = ttk.Treeview(plan_frame, columns=columns, show='headings', selectmode='browse')
        self.user_plan_tree.pack(side="left", fill="both", expand=True)

        self.user_plan_tree.heading("plan_id", text="ID")
        self.user_plan_tree.heading("plan_name", text="Plan Name")
        self.user_plan_tree.heading("meal_type", text="Meal Type")
        self.user_plan_tree.heading("total_calories", text="Total Calories")
        self.user_plan_tree.heading("eaten", text="Eaten")

        self.user_plan_tree.column("plan_id", width=50, anchor='center')
        self.user_plan_tree.column("plan_name", width=200, anchor='center')
        self.user_plan_tree.column("meal_type", width=100, anchor='center')
        self.user_plan_tree.column("total_calories", width=120, anchor='center')
        self.user_plan_tree.column("eaten", width=80, anchor='center')

        self.user_plan_tree.bind('<Double-1>', self.on_double_click_user_plan)

        scrollbar = ttk.Scrollbar(plan_frame, orient="vertical", command=self.user_plan_tree.yview)
        scrollbar.pack(side="left", fill="y")
        self.user_plan_tree.configure(yscrollcommand=scrollbar.set)

        add_plan_button = ttk.Button(self.user_plans_tab, text="Add New Plan",
                                     command=lambda: self.controller.show_page("MakePlanView"))
        add_plan_button.pack(pady=20)

        # ---------------------------
        # All Plans Tab
        # ---------------------------
        self.all_plans_tab = ttk.Frame(self.notebook, style='MainContent.TFrame')
        self.notebook.add(self.all_plans_tab, text="All Plans")

        all_plans_label = ttk.Label(
            self.all_plans_tab,
            text="All Plans in Database",
            font=("Roboto", 16, "bold"),
            foreground=COLOR_TEXT,
            background=COLOR_BACKGROUND
        )
        all_plans_label.pack(pady=10)

        all_plan_frame = ttk.Frame(self.all_plans_tab, style='MainContent.TFrame')
        all_plan_frame.pack(pady=10, padx=20, fill="both", expand=True)

        db_columns = ("plan_id", "plan_name", "meal_type", "total_calories")
        # Allow multiple selection by using selectmode='extended'
        self.db_plan_tree = ttk.Treeview(all_plan_frame, columns=db_columns, show='headings', selectmode='extended')
        self.db_plan_tree.pack(side="left", fill="both", expand=True)

        self.db_plan_tree.heading("plan_id", text="ID")
        self.db_plan_tree.heading("plan_name", text="Plan Name")
        self.db_plan_tree.heading("meal_type", text="Meal Type")
        self.db_plan_tree.heading("total_calories", text="Total Calories")

        self.db_plan_tree.column("plan_id", width=50, anchor='center')
        self.db_plan_tree.column("plan_name", width=200, anchor='center')
        self.db_plan_tree.column("meal_type", width=100, anchor='center')
        self.db_plan_tree.column("total_calories", width=120, anchor='center')

        db_scrollbar = ttk.Scrollbar(all_plan_frame, orient="vertical", command=self.db_plan_tree.yview)
        db_scrollbar.pack(side="left", fill="y")
        self.db_plan_tree.configure(yscrollcommand=db_scrollbar.set)

        # Delete button for plans in PlanDatabase (bulk delete)
        delete_plan_button = ttk.Button(self.all_plans_tab, text="Delete Selected Plans", command=self.delete_selected_plans_from_db)
        delete_plan_button.pack(pady=20)

        self.load_plans()
        self.load_all_plans()

    def load_plans(self):
        # Load user plans for the selected date
        self.user_plan_tree.delete(*self.user_plan_tree.get_children())
        self.controller.db_manager.connect()
        plans = self.controller.db_manager.read(
            table="UserPlan",
            columns=["plan_id", "plan_name", "meal_type", "total_calories", "eaten"],
            conditions={"date": self.selected_date},
            single=False
        )
        self.controller.db_manager.disconnect()

        for plan in plans:
            plan_id, plan_name, meal_type, total_calories, eaten = plan
            eaten_status = "Yes" if eaten else "No"
            self.user_plan_tree.insert("", tk.END, values=(plan_id, plan_name, meal_type, total_calories, eaten_status))

    def load_all_plans(self):
        # Load all plans from PlanDatabase
        self.db_plan_tree.delete(*self.db_plan_tree.get_children())
        self.controller.db_manager.connect()
        all_plans = self.controller.db_manager.read(
            table="PlanDatabase",
            columns=["plan_id", "plan_name", "meal_type", "total_calories"],
            conditions=None,
            single=False
        )
        self.controller.db_manager.disconnect()

        for p in all_plans:
            plan_id, plan_name, meal_type, total_calories = p
            self.db_plan_tree.insert("", tk.END, values=(plan_id, plan_name, meal_type, total_calories))

    def on_double_click_user_plan(self, event):
        item = self.user_plan_tree.identify_row(event.y)
        column = self.user_plan_tree.identify_column(event.x)
        if not item or not column:
            return

        # 'eaten' column is #5
        if column == '#5':
            self.toggle_eaten_status(item)
        else:
            self.show_plan_details(item)

    def toggle_eaten_status(self, item):
        current_eaten = self.user_plan_tree.set(item, "eaten")
        new_eaten = 0 if current_eaten == "Yes" else 1

        plan_id = int(self.user_plan_tree.set(item, "plan_id"))
        self.controller.db_manager.connect()
        self.controller.db_manager.update(
            table="UserPlan",
            data={"eaten": new_eaten},
            conditions={"plan_id": plan_id, "date": self.selected_date}
        )
        self.controller.db_manager.disconnect()

        self.user_plan_tree.set(item, "eaten", "Yes" if new_eaten else "No")
        self.controller.sidebar_right.update_calorie_meter()

    def show_plan_details(self, item):
        plan_id = int(self.user_plan_tree.set(item, "plan_id"))
        plan_name = self.user_plan_tree.set(item, "plan_name")

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
            font=("Roboto", 16, "bold"),
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

    def delete_selected_plans_from_db(self):
        # Get all selected items from the db_plan_tree
        selection = self.db_plan_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select one or more plans to delete.")
            return

        # Collect plan_ids and names
        plan_ids = []
        plans_to_delete = []
        for item in selection:
            plan_id = int(self.db_plan_tree.set(item, "plan_id"))
            plan_name = self.db_plan_tree.set(item, "plan_name")
            plans_to_delete.append((plan_id, plan_name))
            plan_ids.append(plan_id)

        # Check if any selected plan is used in UserPlan
        self.controller.db_manager.connect()
        for plan_id, plan_name in plans_to_delete:
            userplan_entry = self.controller.db_manager.read("UserPlan", ["plan_id"], {"plan_id": plan_id}, True)
            if userplan_entry:
                # Found a plan that is referenced in UserPlan
                self.controller.db_manager.disconnect()
                messagebox.showwarning("Cannot Delete", f"Plan '{plan_name}' (ID: {plan_id}) is currently referenced in UserPlan and cannot be deleted.")
                return
        self.controller.db_manager.disconnect()

        # If we reached here, none of the selected plans are referenced in UserPlan
        # Confirm bulk deletion
        plan_names_str = ", ".join([p[1] for p in plans_to_delete])
        response = messagebox.askyesno("Confirm Deletion",
                                       f"Are you sure you want to delete the following plans?\n{plan_names_str}")
        if not response:
            return

        # Delete all selected plans from PlanDatabase
        self.controller.db_manager.connect()
        for plan_id, plan_name in plans_to_delete:
            self.controller.db_manager.delete("PlanDatabase", {"plan_id": plan_id})
        self.controller.db_manager.disconnect()

        messagebox.showinfo("Deleted", "Selected plans have been deleted from the database.")
        self.load_all_plans()
