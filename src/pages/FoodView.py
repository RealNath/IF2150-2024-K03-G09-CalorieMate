# src/pages/FoodView.py
import tkinter as tk
from tkinter import messagebox
from logic.DatabaseManager import DatabaseManager
from pages.editFood import EditFoodView

Database = 'src/database/database.db'
db = DatabaseManager(Database)

class FoodView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.food_list_frame = tk.Frame(self)
        self.food_list_frame.pack(expand=True, fill=tk.BOTH)
        self.create_widgets()
        self.load_foods()

    def create_widgets(self):
        add_food_button = tk.Button(self, text="Add New Food", command=lambda: self.controller.show_page("MakeFoodView"))
        add_food_button.pack(pady=10)

    def load_foods(self):
        for widget in self.food_list_frame.winfo_children():
            widget.destroy()

        db.connect()
        foods = db.read("FoodDatabase", ["food_id", "name", "calories", "protein", "carbs", "total_fat", "cholesterol", "saturated_fat", "sodium", "fiber", "sugar"], None, False)
        db.disconnect()

        for food in foods:
            food_id, name, calories, protein, carbs, total_fat, cholesterol, saturated_fat, sodium, fiber, sugar = food
            food_label = tk.Label(self.food_list_frame, text=f"Food: {name} - Calories: {calories} | Protein: {protein} | Carbs: {carbs}")
            food_label.pack(anchor=tk.W, padx=10, pady=5)

            nutritional_facts = f"Fat: {total_fat} | Cholesterol: {cholesterol} | Sodium: {sodium} | Fiber: {fiber} | Sugar: {sugar}"
            nutritional_label = tk.Label(self.food_list_frame, text=nutritional_facts)
            nutritional_label.pack(anchor=tk.W, padx=10, pady=5)

            delete_button = tk.Button(self.food_list_frame, text="Delete", command=lambda fid=food_id: self.delete_food(fid))
            delete_button.pack(pady=5)
            
            edit_button = tk.Button(self.food_list_frame, text="Edit", command=lambda fid=food_id: self.edit_food(fid))
            edit_button.pack(pady=5)

    def delete_food(self, food_id):
        response = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this food item?")
        if response:
            db.connect()
            db.delete("FoodDatabase", {"food_id": food_id})
            db.disconnect()
            self.load_foods()
            
            
    def edit_food(self, food_id):
        # Navigate to editFood
        self.controller.main_content.show_page("editFood.EditFoodView", food_id=food_id)
