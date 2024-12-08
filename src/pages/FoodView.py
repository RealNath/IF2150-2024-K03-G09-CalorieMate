import tkinter as tk
from logic.DatabaseManager import DatabaseManager
import sqlite3

Database = 'src/database/database.db'  # Path to database
db = DatabaseManager(Database)

class FoodView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.food_list_frame = tk.Frame(self)  # Frame to display food list
        self.food_list_frame.pack(expand=True, fill=tk.BOTH)
        self.create_widgets()

    def create_widgets(self):
        # Button to add new food
        add_food_button = tk.Button(self, text="Add New Food", command=lambda: self.controller.show_page("MakeFoodView"))
        add_food_button.pack(pady=10)

    def load_foods(self):
        # Clear any existing widgets (food items)
        for widget in self.food_list_frame.winfo_children():
            widget.destroy()

        # Load food data from the database
        db.connect()

        foods = db.read("FoodDatabase", ["food_id, name, calories, protein, carbs, total_fat, cholesterol, saturated_fat, sodium, fiber, sugar"], None, False)

        for food in foods:
            food_id, name, calories, protein, carbs, total_fat, cholesterol, saturated_fat, sodium, fiber, sugar = food
            food_label = tk.Label(self.food_list_frame, text=f"Food: {name} - Calories: {calories} | Protein: {protein} | Carbs: {carbs}")
            food_label.pack(anchor=tk.W, padx=10, pady=5)
            
            # Nutritional Facts
            nutritional_facts = f"Fat: {total_fat} | Cholesterol: {cholesterol} | Sodium: {sodium} | Fiber: {fiber} | Sugar: {sugar}"
            nutritional_label = tk.Label(self.food_list_frame, text=nutritional_facts)
            nutritional_label.pack(anchor=tk.W, padx=10, pady=5)

            # Delete Button
            delete_button = tk.Button(self.food_list_frame, text="Delete", command=lambda food_id=food_id: self.delete_food(food_id))
            delete_button.pack(pady=5)

        db.disconnect()

    def delete_food(self, food_id):
        # Confirm before deleting the food item
        response = tk.messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this food item?")
        if response:
            # Delete the food from the database
            db.connect()
            db.delete("FoodDatabase", {"food_id": food_id})
            db.disconnect()

            # Reload the food list to reflect the deletion
            self.load_foods()
