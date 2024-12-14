# src/pages/MakeFoodView.py
import tkinter as tk
import tkinter.messagebox as MessageBox
from logic.DatabaseManager import DatabaseManager

Database = 'src/database/database.db'
db = DatabaseManager(Database)

class MakeFoodView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        back_button = tk.Button(self, text="Back to Food View", command=lambda: self.controller.show_page("FoodView"), font=("Comic Sans MS", 10), background="blue", foreground="black")
        back_button.pack(pady=10)

        tk.Label(self, text="Food Name:", font=("Verdana", 10, "bold" ), background="light grey", foreground="black").pack()
        self.name_entry = tk.Entry(self)
        self.name_entry.pack()

        tk.Label(self, text="Calories:", font=("Verdana", 10, "bold" ), background="light grey", foreground="black").pack()
        self.calories_entry = tk.Entry(self)
        self.calories_entry.pack()

        tk.Label(self, text="Protein (g):", font=("Verdana", 10, "bold" ), background="light grey", foreground="black").pack()
        self.protein_entry = tk.Entry(self)
        self.protein_entry.pack()

        tk.Label(self, text="Carbs (g):", font=("Verdana", 10, "bold" ), background="light grey", foreground="black").pack()
        self.carbs_entry = tk.Entry(self)
        self.carbs_entry.pack()

        tk.Label(self, text="Total Fat (g):", font=("Verdana", 10, "bold" ), background="light grey", foreground="black").pack()
        self.total_fat_entry = tk.Entry(self)
        self.total_fat_entry.pack()

        tk.Label(self, text="Cholesterol (mg):", font=("Verdana", 10, "bold" ), background="light grey", foreground="black").pack()
        self.cholesterol_entry = tk.Entry(self)
        self.cholesterol_entry.pack()

        tk.Label(self, text="Saturated Fat (g):", font=("Verdana", 10, "bold" ), background="light grey", foreground="black").pack()
        self.saturated_fat_entry = tk.Entry(self)
        self.saturated_fat_entry.pack()

        tk.Label(self, text="Sodium (mg):",font=("Verdana", 10, "bold" ), background="light grey", foreground="black").pack()
        self.sodium_entry = tk.Entry(self)
        self.sodium_entry.pack()

        tk.Label(self, text="Fiber (g):", font=("Verdana", 10, "bold" ), background="light grey", foreground="black").pack()
        self.fiber_entry = tk.Entry(self)
        self.fiber_entry.pack()

        tk.Label(self, text="Sugar (g):", font=("Verdana", 10, "bold" ), background="light grey", foreground="black").pack()
        self.sugar_entry = tk.Entry(self)
        self.sugar_entry.pack()

        add_food_button = tk.Button(self, text="Add Food Item", command=self.add_food_item, font=("Comic Sans MS", 10), background="light green", foreground="black")
        add_food_button.pack(pady=20)

    def add_food_item(self):
        name = self.name_entry.get()
        calories = self.calories_entry.get()
        protein = self.protein_entry.get()
        carbs = self.carbs_entry.get()
        total_fat = self.total_fat_entry.get()
        cholesterol = self.cholesterol_entry.get()
        saturated_fat = self.saturated_fat_entry.get()
        sodium = self.sodium_entry.get()
        fiber = self.fiber_entry.get()
        sugar = self.sugar_entry.get()

        try:
            calories = int(calories)
            protein = float(protein)
            carbs = float(carbs)
            total_fat = float(total_fat)
            cholesterol = float(cholesterol)
            saturated_fat = float(saturated_fat)
            sodium = float(sodium)
            fiber = float(fiber)
            sugar = float(sugar)
        except ValueError:
            MessageBox.showerror("Input Error", "Please enter valid numerical values for nutritional info.")
            return

        db.connect()
        db.create("FoodDatabase", {
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
        })
        db.disconnect()

        MessageBox.showinfo("Success", f"Food item '{name}' has been added successfully!")

        # Clear entries
        self.name_entry.delete(0, tk.END)
        self.calories_entry.delete(0, tk.END)
        self.protein_entry.delete(0, tk.END)
        self.carbs_entry.delete(0, tk.END)
        self.total_fat_entry.delete(0, tk.END)
        self.cholesterol_entry.delete(0, tk.END)
        self.saturated_fat_entry.delete(0, tk.END)
        self.sodium_entry.delete(0, tk.END)
        self.fiber_entry.delete(0, tk.END)
        self.sugar_entry.delete(0, tk.END)

        self.controller.show_page("FoodView")
