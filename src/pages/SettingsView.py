#Import-import apalah itu dari sini
import tkinter as tk

#Code mulai dari sini
class SettingsView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller  # Store the controller (MainApp)
        
        #Lanjutkan code