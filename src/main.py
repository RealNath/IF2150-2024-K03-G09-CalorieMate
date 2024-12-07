#Import-import apalah itu dari sini
import tkinter as tk
import csv #kalau pake csv, untuk baca file csv nya
from pages.ArticleView import ArticleView
from pages.FoodView import FoodView
from pages.HistoryView import HistoryView
from pages.MakePlanView import MakePlanView
from pages.MakeFoodView import MakeFood
from pages.PlanView import PlanView
from pages.ProfileView import ProfileView
from pages.SettingsView import SettingsView


#Code mulai dari sini

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CalorieMate - Homepage")
        self.geometry("1280x720")

        self.frames = {}  # Dictionary untuk menyimpan semua halaman
        self.initialize_pages()

        self.show_page("FoodView")  # Halaman awal

    def initialize_pages(self):
        container = tk.Frame(self)
        container.pack(fill=tk.BOTH, expand=True)

        # Menambahkan halaman FoodView
        self.frames["FoodView"] = FoodView(parent=container, controller=self)
        self.frames["FoodView"].grid(row=0, column=0, sticky="nsew")

        # Menambahkan halaman MakeFood
        self.frames["MakeFoodView"] = MakeFood(parent=container, controller=self)
        self.frames["MakeFoodView"].grid(row=0, column=0, sticky="nsew")

    def show_page(self, page_name):
        frame = self.frames[page_name]
        if page_name == "FoodView":  # Refresh data saat kembali ke FoodView
            frame.load_foods()
        frame.tkraise()



if __name__ == "__main__":
    app = MainApp()
    app.mainloop()