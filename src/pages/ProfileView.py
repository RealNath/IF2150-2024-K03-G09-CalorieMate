# src/pages/ProfileView.py
import tkinter as tk
from tkinter import ttk, messagebox
from logic.DatabaseManager import DatabaseManager
from config import COLOR_BACKGROUND, COLOR_TEXT
import tkinter.filedialog as fd
from PIL import Image, ImageTk

Database = 'src/database/database.db'
db = DatabaseManager(Database)

class ProfileView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BACKGROUND)
        self.controller = controller
        self.user_id = 1
        self.create_widgets()
        self.load_user_profile()

    def create_widgets(self):
        title_label = ttk.Label(self, text="Profile", font=("Roboto", 16, "bold"), foreground=COLOR_TEXT, background=COLOR_BACKGROUND)
        title_label.pack(pady=10)

        profile_frame = ttk.Frame(self, style='MainContent.TFrame')
        profile_frame.pack(pady=10, padx=20, fill="x")

        name_label = ttk.Label(profile_frame, text="Name:", font=("Roboto", 12),
                               foreground=COLOR_TEXT, background=COLOR_BACKGROUND)
        name_label.grid(row=0, column=0, sticky="w", pady=5)
        self.name_entry = ttk.Entry(profile_frame, width=30)
        self.name_entry.grid(row=0, column=1, pady=5, padx=10)

        save_button = ttk.Button(self, text="Save Changes", command=self.save_profile)
        save_button.pack(pady=20)
        
        # Add a button to select image
        tk.Label(self, text="Profile Picture: (click button to select image)", bg=COLOR_BACKGROUND, fg=COLOR_TEXT).pack(pady=5)
        self.profile_image_button = tk.Button(self, text="Select Image", command=self.select_image)
        self.profile_image_button.pack(pady=5)
        self.image_path_var = tk.StringVar()

    def load_user_profile(self):
        db.connect()
        user = db.read("UserPreference", ["name", "profile_image"], {"user_id": self.user_id}, True)
        db.disconnect()

        if user:
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, user[0])
            if user[1]:
                self.image_path_var.set(user[1])
        else:
            messagebox.showerror("Error", "Failed to load user profile.")

    def select_image(self):
        path = fd.askopenfilename(
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])
        if path:
            self.image_path_var.set(path)

    def save_profile(self):
        new_name = self.name_entry.get().strip()
        image_path = self.image_path_var.get()

        if not new_name:
            messagebox.showwarning("Input Error", "Name cannot be empty.")
            return

        db.connect()
        db.update("UserPreference", {"name": new_name, "profile_image": image_path}, {"user_id": self.user_id})
        db.disconnect()

        messagebox.showinfo("Success", "Profile updated successfully.")

        if hasattr(self.controller, 'sidebar_right') and hasattr(self.controller.sidebar_right, 'user_info'):
            self.controller.sidebar_right.user_info.load_user_info()
