#Import-import apalah itu dari sini
import tkinter as tk

Database = 'src/database/database.db' # Path to database

#Code mulai dari sini
class HistoryView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller  # Store the controller (MainApp)
        
        #Lanjutkan code