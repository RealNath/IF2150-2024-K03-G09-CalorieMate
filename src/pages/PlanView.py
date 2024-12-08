import tkinter as tk
from logic.DatabaseManager import DatabaseManager
from datetime import date
from tkinter import messagebox
from tkinter import ttk  # Import ttk for Combobox

Database = 'src/database/database.db'  # Path to database
db = DatabaseManager(Database)

class PlanView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.dropdown = None  # Variable to store the dropdown reference
        self.confirm_button = None  # Variable to store the confirm button reference
        self.plan_selection_label = None  # Variable to store the plan selection label reference
        self.create_widgets()

    def create_widgets(self):
        today = date.today().isoformat()

        # Clear previous content
        for widget in self.winfo_children():
            widget.destroy()

        db.connect()
        
        plans = db.read("UserPlan", ["plan_name, meal_type"], {"date" : today}, False)

        if plans:
            for plan in plans:
                plan_label = tk.Label(self, text=f"Plan: {plan[0]}, Meal Type: {plan[1]}")
                plan_label.pack()

                # Add a delete button for each plan
                delete_button = tk.Button(self, text="Delete", command=lambda plan_name=plan[0]: self.delete_plan(plan_name))
                delete_button.pack(pady=5)
        else:
            no_plan_label = tk.Label(self, text="No plans for today.")
            no_plan_label.pack()

            # 'Make a Plan' Button
            make_plan_button = tk.Button(self, text="Make a Plan", command=lambda: self.controller.show_page("MakePlanView"))
            make_plan_button.pack(pady=10)

        # 'Add a Plan' Button
        add_plan_button = tk.Button(self, text="Add a Plan", command=self.add_plan)
        add_plan_button.pack(pady=10)

        db.disconnect()

    def add_plan(self):
        # Fetch all available plans from PlanDatabase
        db.connect()

        available_plans = db.read("PlanDatabase", ["plan_name"], None, False)

        if not available_plans:
            messagebox.showwarning("No Plans Available", "There are no available plans in the PlanDatabase.")
            db.disconnect()
            return

        # Extract the plan names from the fetched data
        plan_names = [plan[0] for plan in available_plans]

        # Check if the plan selection label already exists, if so, don't create another
        if self.plan_selection_label:
            self.plan_selection_label.destroy()  # Remove the old label if it exists

        # Create a new label for selecting a plan
        self.plan_selection_label = tk.Label(self, text="Select a plan:")
        self.plan_selection_label.pack(pady=5)

        # Check if the dropdown already exists, if so, don't create another
        if self.dropdown:
            self.dropdown.destroy()  # Remove the old dropdown if it exists

        # Create a new dropdown (Combobox) to select the plan
        self.dropdown = ttk.Combobox(self, values=plan_names)
        self.dropdown.set(plan_names[0])  # Set the default value to the first plan
        self.dropdown.pack(pady=5)

        # Check if the confirm button already exists, if so, don't create another
        if self.confirm_button:
            self.confirm_button.destroy()  # Remove the old confirm button if it exists

        # Button to confirm selection and add the plan
        self.confirm_button = tk.Button(self, text="Add", command=lambda: self.confirm_add_plan())
        self.confirm_button.pack(pady=10)

    def confirm_add_plan(self):
        selected_plan_name = self.dropdown.get()

        # Validate if a plan was selected
        if not selected_plan_name:
            messagebox.showwarning("Invalid Selection", "Please select a plan.")
            return

        # Fetch details for the selected plan from PlanDatabase
        db.connect()
        selected_plan = db.read("PlanDatabase", ["meal_type, food_items, total_calories"], {"plan_name" : selected_plan_name}, True)

        # Insert the selected plan into UserPlan
        today = date.today().isoformat()
        meal_type = selected_plan[0]
        total_calories = selected_plan[2]
        eaten = False  # Placeholder value

        db.create("UserPlan", {"plan_name": selected_plan_name, "date": today, "meal_type": meal_type, "total_calories": total_calories, "eaten": eaten})

        # Show confirmation
        messagebox.showinfo("Plan Added", f"The plan '{selected_plan_name}' has been added to your plan for today.")
        db.disconnect()

        # Refresh PlanView page with updated content
        self.controller.show_page("PlanView")

    def delete_plan(self, plan_name):
        # Confirm the deletion
        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete the plan '{plan_name}'?")
        if confirm:
            # Delete the selected plan from the database
            db.connect()

            db.delete("UserPlan", {"plan_name" : plan_name})
            
            db.disconnect()

            # Show confirmation message
            messagebox.showinfo("Plan Deleted", f"The plan '{plan_name}' has been deleted.")

            # Refresh the PlanView to reflect the change
            self.create_widgets()  # Refresh content on the page
