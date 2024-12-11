# src/pages/SettingsView.py
import tkinter as tk
from tkinter import ttk, messagebox
from logic.DatabaseManager import DatabaseManager

Database = 'src/database/database.db'  # Path to database
db = DatabaseManager(Database)

class SettingsView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.user_id = 1  # Assuming single user with ID 1
        self.create_widgets()
        self.load_settings()

    def create_widgets(self):
        # Title Label
        title_label = ttk.Label(self, text="Settings", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        # Frame for settings
        settings_frame = ttk.Frame(self)
        settings_frame.pack(pady=10, padx=20, fill="x")

        # Notification Toggle
        self.notification_var = tk.IntVar()
        notification_check = ttk.Checkbutton(settings_frame, text="Enable Notifications",
                                            variable=self.notification_var)
        notification_check.grid(row=0, column=0, sticky="w", pady=5)

        # Dark Mode Toggle (Optional)
        self.dark_mode_var = tk.IntVar()
        dark_mode_check = ttk.Checkbutton(settings_frame, text="Enable Dark Mode",
                                         variable=self.dark_mode_var)
        dark_mode_check.grid(row=1, column=0, sticky="w", pady=5)

        # Save Button
        save_button = ttk.Button(self, text="Save Settings", command=self.save_settings)
        save_button.pack(pady=20)

    def load_settings(self):
        db.connect()
        settings = db.read("UserPreference", ["notification_enabled", "DarkMode"], {"user_id": self.user_id}, True)
        db.disconnect()

        if settings:
            self.notification_var.set(settings[0])
            self.dark_mode_var.set(settings[1])
        else:
            messagebox.showerror("Error", "Failed to load settings.")

    def save_settings(self):
        notification = self.notification_var.get()
        dark_mode = self.dark_mode_var.get()

        db.connect()
        db.update("UserPreference", {"notification_enabled": notification, "DarkMode": dark_mode}, {"user_id": self.user_id})
        db.disconnect()

        messagebox.showinfo("Success", "Settings updated successfully.")

        # Optional: Apply dark mode changes immediately
        if dark_mode:
            self.controller.enable_dark_mode()
        else:
            self.controller.disable_dark_mode()
