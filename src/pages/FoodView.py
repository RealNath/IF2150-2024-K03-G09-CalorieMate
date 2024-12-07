import tkinter as tk
import sqlite3

Database = 'src/database/database.db' # Path to database

class FoodView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.food_list_frame = tk.Frame(self)  # Frame untuk daftar makanan
        self.food_list_frame.pack()
        self.create_widgets()

    def create_widgets(self):
        add_food_button = tk.Button(self, text="Add New Food", command=lambda: self.controller.show_page("MakeFoodView"))
        add_food_button.pack(pady=10)
        del_food_button = tk.Button(self, text="Delete Food", command=lambda: self.controller.show_page("DeleteFoodView"))

    def load_foods(self):
        # Hapus data sebelumnya
        for widget in self.food_list_frame.winfo_children():
            widget.destroy()

        # Muat data dari database
        conn = sqlite3.connect('src/database/database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name, calories, protein, carbs, total_fat, cholesterol, saturated_fat, sodium, fiber, sugar FROM FoodDatabase")
        foods = cursor.fetchall()

        for food in foods:
            tk.Label(self.food_list_frame, text=f"Food: {food[0]}").pack()
            nutritional_facts = f"Calories: {food[1]} | Protein: {food[2]} | Carbs: {food[3]} | Fat: {food[4]} | Cholesterol: {food[5]} | Saturated Fat: {food[6]} | Sodium: {food[7]} | Fiber: {food[8]} | Sugar: {food[9]}"
            tk.Label(self.food_list_frame, text=nutritional_facts).pack()

        conn.close()
