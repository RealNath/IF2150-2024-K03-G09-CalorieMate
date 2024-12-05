import tkinter as tk
import sqlite3

class FoodView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        # 'Add New Food' Button
        add_food_button = tk.Button(self, text="Add New Food", command=lambda: self.controller.show_page("MakeFoodView"))
        add_food_button.pack(pady=10)

        # Connect to database to get food items
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute("SELECT name, calories, protein, carbs, total_fat, cholesterol, saturated_fat, sodium, fiber, sugar FROM FoodDatabase")
        foods = cursor.fetchall()

        # Display each food item with nutritional facts
        for food in foods:
            food_name = tk.Label(self, text=f"Food: {food[0]}")
            food_name.pack()

            # Create a table-like label for nutritional facts
            nutritional_facts = f"Calories: {food[1]} kcal | Protein: {food[2]} g | Carbs: {food[3]} g | Fat: {food[4]} g | Cholesterol: {food[5]} mg | Saturated Fat: {food[6]} g | Sodium: {food[7]} mg | Fiber: {food[8]} g | Sugar: {food[9]} g"
            nutrition_label = tk.Label(self, text=nutritional_facts)
            nutrition_label.pack()

        conn.close()
