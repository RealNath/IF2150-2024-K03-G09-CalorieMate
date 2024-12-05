#Import-import apalah itu dari sini
import tkinter as tk
import csv #kalau pake csv, untuk baca file csv nya
from pages.ArticleView import ArticleView
from pages.FoodView import FoodView
from pages.HistoryView import HistoryView
from pages.MakePlanView import MakePlanView
from pages.PlanView import PlanView
from pages.ProfileView import ProfileView
from pages.SettingsView import SettingsView


#Code mulai dari sini

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CalorieMate - Homepage")
        self.geometry("1280x720") #Window Size
        #Lanjutkan Code
        
        
        
if __name__ == "__main__":
    app = MainApp()
    app.mainloop()