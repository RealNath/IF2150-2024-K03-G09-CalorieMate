import tkinter as tk
import tkinter.messagebox as MessageBox
from logic.DatabaseManager import DatabaseManager
import sqlite3

Database = 'src/database/database.db' # Path to database
db = DatabaseManager(Database)

class MakeFood(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        # Tambahkan tombol untuk kembali ke FoodView
        back_button = tk.Button(self, text="Back to Food View", command=lambda: self.controller.show_page("FoodView"))
        back_button.pack(pady=10)
        
        # Food Name
        tk.Label(self, text="Food Name:").pack()
        self.name_entry = tk.Entry(self)
        self.name_entry.pack()

        # Calories
        tk.Label(self, text="Calories:").pack()
        self.calories_entry = tk.Entry(self)
        self.calories_entry.pack()

        # Protein
        tk.Label(self, text="Protein (g):").pack()
        self.protein_entry = tk.Entry(self)
        self.protein_entry.pack()

        # Carbs
        tk.Label(self, text="Carbs (g):").pack()
        self.carbs_entry = tk.Entry(self)
        self.carbs_entry.pack()

        # Total Fat
        tk.Label(self, text="Total Fat (g):").pack()
        self.total_fat_entry = tk.Entry(self)
        self.total_fat_entry.pack()

        # Cholesterol
        tk.Label(self, text="Cholesterol (mg):").pack()
        self.cholesterol_entry = tk.Entry(self)
        self.cholesterol_entry.pack()

        # Saturated Fat
        tk.Label(self, text="Saturated Fat (g):").pack()
        self.saturated_fat_entry = tk.Entry(self)
        self.saturated_fat_entry.pack()

        # Sodium
        tk.Label(self, text="Sodium (mg):").pack()
        self.sodium_entry = tk.Entry(self)
        self.sodium_entry.pack()

        # Fiber
        tk.Label(self, text="Fiber (g):").pack()
        self.fiber_entry = tk.Entry(self)
        self.fiber_entry.pack()

        # Sugar
        tk.Label(self, text="Sugar (g):").pack()
        self.sugar_entry = tk.Entry(self)
        self.sugar_entry.pack()

        # 'Add Food Item' Button
        add_food_button = tk.Button(self, text="Add Food Item", command=self.add_food_item)
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
            print("Please enter valid numerical values.")
            return

        # Update the FoodDatabase
        db.connect()
        db.create("FoodDatabase", {"name" : name, "calories" : calories, "protein" : protein, "carbs" : carbs, "total_fat" : total_fat, "cholesterol" : cholesterol, "saturated_fat" : saturated_fat, "sodium" : sodium, "fiber" : fiber, "sugar" : sugar})
        db.disconnect()
        print(f"Added food item '{name}' to the FoodDatabase")

        # Kosongkan semua entri
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

        # Tampilkan pesan konfirmasi
        MessageBox.showinfo("Success", f"Food item '{name}' has been added successfully!")

        # Kembali ke halaman sebelumnya (FoodView)
        self.controller.show_page("FoodView")

