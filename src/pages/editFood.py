# src/pages/editFood.py
import tkinter as tk
import tkinter.messagebox as MessageBox
from logic.DatabaseManager import DatabaseManager

Database = 'src/database/database.db'
db = DatabaseManager(Database)

class EditFoodView(tk.Frame):
    def __init__(self, parent, controller, food_id):
        super().__init__(parent)
        self.controller = controller
        self.food_id = food_id
        self.create_widgets()
        self.load_food_item()

    def create_widgets(self):
        back_button = tk.Button(self, text="Back to Food View", command=lambda: self.controller.show_page("FoodView"))
        back_button.pack(pady=10)

        tk.Label(self, text="Food Name:").pack()
        self.name_entry = tk.Entry(self)
        self.name_entry.pack()

        tk.Label(self, text="Calories:").pack()
        self.calories_entry = tk.Entry(self)
        self.calories_entry.pack()

        tk.Label(self, text="Protein (g):").pack()
        self.protein_entry = tk.Entry(self)
        self.protein_entry.pack()

        tk.Label(self, text="Carbs (g):").pack()
        self.carbs_entry = tk.Entry(self)
        self.carbs_entry.pack()

        tk.Label(self, text="Total Fat (g):").pack()
        self.total_fat_entry = tk.Entry(self)
        self.total_fat_entry.pack()

        tk.Label(self, text="Cholesterol (mg):").pack()
        self.cholesterol_entry = tk.Entry(self)
        self.cholesterol_entry.pack()

        tk.Label(self, text="Saturated Fat (g):").pack()
        self.saturated_fat_entry = tk.Entry(self)
        self.saturated_fat_entry.pack()

        tk.Label(self, text="Sodium (mg):").pack()
        self.sodium_entry = tk.Entry(self)
        self.sodium_entry.pack()

        tk.Label(self, text="Fiber (g):").pack()
        self.fiber_entry = tk.Entry(self)
        self.fiber_entry.pack()

        tk.Label(self, text="Sugar (g):").pack()
        self.sugar_entry = tk.Entry(self)
        self.sugar_entry.pack()

        save_button = tk.Button(self, text="Save Changes", command=self.save_food_item)
        save_button.pack(pady=20)

    def load_food_item(self):
        db.connect()
        food = db.read("FoodDatabase", 
                       ["name", "calories", "protein", "carbs", "total_fat", "cholesterol", "saturated_fat", "sodium", "fiber", "sugar"],
                       {"food_id": self.food_id}, True)
        db.disconnect()
        if food:
            (name, calories, protein, carbs, total_fat, cholesterol, saturated_fat, sodium, fiber, sugar) = food
            self.name_entry.insert(0, name)
            self.calories_entry.insert(0, str(calories))
            self.protein_entry.insert(0, str(protein))
            self.carbs_entry.insert(0, str(carbs))
            self.total_fat_entry.insert(0, str(total_fat))
            self.cholesterol_entry.insert(0, str(cholesterol))
            self.saturated_fat_entry.insert(0, str(saturated_fat))
            self.sodium_entry.insert(0, str(sodium))
            self.fiber_entry.insert(0, str(fiber))
            self.sugar_entry.insert(0, str(sugar))
        else:
            MessageBox.showerror("Error", "Food item not found.")
            self.controller.show_page("FoodView")

    def save_food_item(self):
        try:
            name = self.name_entry.get()
            calories = int(self.calories_entry.get())
            protein = float(self.protein_entry.get())
            carbs = float(self.carbs_entry.get())
            total_fat = float(self.total_fat_entry.get())
            cholesterol = float(self.cholesterol_entry.get())
            saturated_fat = float(self.saturated_fat_entry.get())
            sodium = float(self.sodium_entry.get())
            fiber = float(self.fiber_entry.get())
            sugar = float(self.sugar_entry.get())
        except ValueError:
            MessageBox.showerror("Input Error", "Please enter valid numerical values for nutritional info.")
            return

        db.connect()
        db.update("FoodDatabase", {
            "name": name,
            "calories": calories,
            "protein": protein,
            "carbs": carbs,
            "total_fat": total_fat,
            "cholesterol": cholesterol,
            "saturated_fat": saturated_fat,
            "sodium": sodium,
            "fiber": fiber,
            "sugar": sugar
        }, {"food_id": self.food_id})
        db.disconnect()

        MessageBox.showinfo("Success", f"Food item '{name}' has been updated!")
        self.controller.show_page("FoodView")
