# src/pages/FoodView.py
import tkinter as tk
from tkinter import messagebox, ttk
from logic.DatabaseManager import DatabaseManager
from pages.editFood import EditFoodView

Database = 'src/database/database.db'
db = DatabaseManager(Database)

class FoodView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()
        self.load_foods()

    def create_widgets(self):
        top_frame = tk.Frame(self)
        top_frame.pack(fill=tk.X, pady=10)

        add_food_button = tk.Button(top_frame, text="Add New Food", command=lambda: self.controller.show_page("MakeFoodView"), font = ('Comic Sans MS', 10, 'bold'), background='blue', foreground='black')
        add_food_button.pack(side=tk.LEFT, padx=10)

        table_frame = tk.Frame(self)
        table_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        columns = ("id", "name", "calories", "protein", "carbs", "fat", "cholesterol", "sat_fat", "sodium", "fiber", "sugar")

        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings')
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("calories", text="Calories")
        self.tree.heading("protein", text="Protein")
        self.tree.heading("carbs", text="Carbs")
        self.tree.heading("fat", text="Fat")
        self.tree.heading("cholesterol", text="Cholesterol")
        self.tree.heading("sat_fat", text="Sat Fat")
        self.tree.heading("sodium", text="Sodium")
        self.tree.heading("fiber", text="Fiber")
        self.tree.heading("sugar", text="Sugar")

        self.tree.column("id", width=40, anchor=tk.CENTER)
        self.tree.column("name", width=150, anchor=tk.W)
        self.tree.column("calories", width=70, anchor=tk.CENTER)
        self.tree.column("protein", width=70, anchor=tk.CENTER)
        self.tree.column("carbs", width=70, anchor=tk.CENTER)
        self.tree.column("fat", width=70, anchor=tk.CENTER)
        self.tree.column("cholesterol", width=90, anchor=tk.CENTER)
        self.tree.column("sat_fat", width=70, anchor=tk.CENTER)
        self.tree.column("sodium", width=70, anchor=tk.CENTER)
        self.tree.column("fiber", width=70, anchor=tk.CENTER)
        self.tree.column("sugar", width=70, anchor=tk.CENTER)

        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y)

        action_frame = tk.Frame(self)
        action_frame.pack(pady=10)

        edit_button = tk.Button(action_frame, text="Edit Selected", command=self.edit_selected, font = ('Comic Sans MS', 10, 'bold'), background='light green', foreground='white')
        edit_button.pack(side=tk.LEFT, padx=5)

        delete_button = tk.Button(action_frame, text="Delete Selected", command=self.delete_selected, font = ('Comic Sans MS', 10, 'bold'), background='red', foreground='white')
        delete_button.pack(side=tk.LEFT, padx=5)

        # LMAO: Double-click on a row to edit
        self.tree.bind("<Double-1>", self.on_double_click)
        
        # Refactor : Font style
        style = ttk.Style()
        style.configure("Custom.Treeview", font=('Verdana', 10), background='light blue', foreground='black')
        self.tree.configure(style="Custom.Treeview")

    def load_foods(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        db.connect()
        foods = db.read("FoodDatabase", ["food_id", "name", "calories", "protein", "carbs", "total_fat",
                                         "cholesterol", "saturated_fat", "sodium", "fiber", "sugar"], None, False)
        db.disconnect()

        for food in foods:
            (food_id, name, calories, protein, carbs, total_fat, cholesterol,
             saturated_fat, sodium, fiber, sugar) = food
            self.tree.insert("", tk.END, values=(food_id, name, calories, protein, carbs,
                                                 total_fat, cholesterol, saturated_fat,
                                                 sodium, fiber, sugar))

    def delete_selected(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No selection", "Please select a food item to delete.")
            return

        food_id = self.tree.item(selected_item, "values")[0]
        response = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this food item?")
        if response:
            db.connect()
            db.delete("FoodDatabase", {"food_id": food_id})
            db.disconnect()
            self.load_foods()

    def edit_selected(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No selection", "Please select a food item to edit.")
            return
        food_id = self.tree.item(selected_item, "values")[0]
        self.controller.main_content.show_page("editFood.EditFoodView", food_id=food_id)

    def on_double_click(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return
        food_id = self.tree.item(selected_item, "values")[0]
        self.controller.main_content.show_page("editFood.EditFoodView", food_id=food_id)
