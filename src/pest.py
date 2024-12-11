import customtkinter as ctk
from logic.DatabaseManager import DatabaseManager
from datetime import date
from tkinter import messagebox
import json
from tkinter import ttk  # For Combobox

Database = 'src/database/database.db'
db = DatabaseManager(Database)

class MealPlanCard(ctk.CTkFrame):
    def __init__(self, parent, plan_data, *args, **kwargs):
        super().__init__(parent, fg_color="#FF5F5F", *args, **kwargs)
        self.grid_columnconfigure(0, weight=1)  # Allow text to stretch
        self.expanded = False  # Track whether the card is expanded or not
        self.plan_data = plan_data

        # Header (Clickable to Expand/Collapse)
        self.header = ctk.CTkButton(
            self,
            text=f"Plan : {plan_data[1]}",
            font=("Arial", 16, "bold"),
            fg_color="#FF5F5F",
            text_color="white",
            corner_radius=0,
            command=self.toggle_expand
        )
        self.header.grid(row=0, column=0, sticky="ew", pady=5)
    
        # Hidden Content (Initially Collapsed)
        self.content_frame = ctk.CTkFrame(self, fg_color="#FF5F5F")
        self.content_frame.grid(row=1, column=0, sticky="ew", padx=10)
        self.content_frame.grid_remove()  # Hide initially

        db.connect()
        foods = db.read("PlanDatabase", ["food_items"], {"plan_name": plan_data[1]}, True)
        foods = json.loads(foods[0])

        # Meal Type and Calories
        ctk.CTkLabel(self.content_frame, text=f"Meal Type : {plan_data[3]}", font=("Arial", 14), text_color="white").grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(self.content_frame, text=f"Calories : {plan_data[4]}", font=("Arial", 14), text_color="white").grid(row=1, column=0, sticky="w", pady=(5, 10))

        # Food Information
        ctk.CTkLabel(self.content_frame, text="Food Information :", font=("Arial", 14, "italic"), text_color="white").grid(row=2, column=0, sticky="w", pady=(5, 0))
        for index, food in enumerate(foods, start=3):
            ctk.CTkLabel(self.content_frame, text=f"• {food}", font=("Arial", 14), text_color="white").grid(row=index, column=0, sticky="w", padx=20)

        # Action Buttons
        button_frame = ctk.CTkFrame(self.content_frame, fg_color="#FF5F5F")  # Match background color
        button_frame.grid(row=index + 1, column=0, pady=10, sticky="e")

        ctk.CTkButton(button_frame, text="Eat", fg_color="#5F9EFF").pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Edit", fg_color="#5F9EFF").pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Delete", fg_color="#5F9EFF", command=lambda plan_id=plan_data[0], plan_name=plan_data[1]: self.delete_plan(plan_id, plan_name)).pack(side="left", padx=5)

    def toggle_expand(self):
        """Toggle the visibility of the content frame."""
        if self.expanded:
            self.content_frame.grid_remove()  # Hide the content
        else:
            self.content_frame.grid()  # Show the content
        self.expanded = not self.expanded  # Toggle state

    def add_plan(self):
        db.connect()
        available_plans = db.read("PlanDatabase", ["plan_name"], None, False)

        if not available_plans:
            messagebox.showwarning("No Plans Available", "There are no available plans in the PlanDatabase.")
            db.disconnect()
            return

        plan_names = [plan[0] for plan in available_plans]

        # Create a new popup window
        popup = ctk.CTkToplevel(self)
        popup.title("Add Plan")
        popup.geometry("400x300")
        popup.configure(fg_color="#1E1E2F")

        # Plan selection label
        plan_selection_label = ctk.CTkLabel(popup, text="Select a plan:", text_color="white", font=("Arial", 14))
        plan_selection_label.pack(pady=10)

        # Dropdown menu for selecting a plan
        dropdown = ttk.Combobox(popup, values=plan_names, font=("Arial", 12))
        dropdown.set(plan_names[0])
        dropdown.pack(pady=10)

        # Confirm button
        confirm_button = ctk.CTkButton(
            popup, 
            text="Add", 
            fg_color="#293241",
            hover_color="#3C3F51",
            text_color="white",
            font=("Arial", 12),
            command=lambda: MealPlanCard.confirm_add_plan(self, popup, dropdown.get())
        )
        confirm_button.pack(pady=20)

    def confirm_add_plan(self, popup, selected_plan_name):
        if not selected_plan_name:
            messagebox.showwarning("Invalid Selection", "Please select a plan.")
            return

        db.connect()
        selected_plan = db.read(
            "PlanDatabase", 
            ["meal_type", "food_items", "total_calories"], 
            {"plan_name": selected_plan_name}, 
            True
        )

        if not selected_plan:
            messagebox.showerror("Error", "The selected plan could not be found.")
            db.disconnect()
            return

        today = date.today().isoformat()
        meal_type, _, total_calories = selected_plan
        eaten = False

        db.create("UserPlan", {
            "plan_name": selected_plan_name,
            "date": today,
            "meal_type": meal_type,
            "total_calories": total_calories,
            "eaten": eaten
        })

        messagebox.showinfo("Plan Added", f"The plan '{selected_plan_name}' has been added.")
        db.disconnect()

        popup.destroy()
        self.create_widgets()
    
    def delete_plan(self, plan_id, plan_name):
        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete the plan '{plan_name}'?")
        if confirm:
            db.connect()
            db.delete("UserPlan", {"plan_id": plan_id})
            db.disconnect()

            messagebox.showinfo("Plan Deleted", f"The plan '{plan_name}' has been deleted.")
            self.create_widgets()


class MealPlanApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Meal Plan App")
        self.geometry("400x600")
        self.configure(fg_color="#1E1E2F")  # Background color

        # Main Layout Configuration
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Header
        header = ctk.CTkFrame(self, fg_color="#6A0DAD", height=80)
        header.grid(row=0, column=0, sticky="ew")
        ctk.CTkLabel(header, text="Meal Plans", font=("Arial", 20, "bold"), text_color="white").pack(pady=20)
        ctk.CTkButton(header, text="Add Plan", fg_color="#6A0DAD", text_color="white", command=lambda: MealPlanCard.add_plan(self)).pack(side="right", padx=10, pady=10)

        # Card Container
        card_container = ctk.CTkScrollableFrame(self, fg_color="#1E1E2F")
        card_container.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        today = date.today().isoformat()

        # Add dynamic meal plan cards
        plans = db.read("UserPlan", ["*"], {"date": today}, False)

        for plan in plans:
            card = MealPlanCard(card_container, plan_data=plan)
            card.pack(fill="x", padx=10, pady=10)

        # Navigation Bar
        navbar = ctk.CTkFrame(self, fg_color="#6A0DAD", height=60)
        navbar.grid(row=2, column=0, sticky="ew")
        ctk.CTkButton(navbar, text="Meal Plans", fg_color="#6A0DAD", text_color="white").pack(side="left", padx=10, pady=10)
        ctk.CTkButton(navbar, text="Articles", fg_color="#6A0DAD", text_color="white").pack(side="left", padx=10, pady=10)
        ctk.CTkButton(navbar, text="Foods", fg_color="#6A0DAD", text_color="white").pack(side="left", padx=10, pady=10)
        ctk.CTkButton(navbar, text="Settings", fg_color="#6A0DAD", text_color="white").pack(side="left", padx=10, pady=10)


if __name__ == "__main__":
    app = MealPlanApp()
    app.mainloop()
