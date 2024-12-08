import tkinter as tk
from pages.ArticleView import ArticleView
from pages.FoodView import FoodView
from pages.HistoryView import HistoryView
from pages.MakePlanView import MakePlanView
from pages.MakeFoodView import MakeFood
from pages.PlanView import PlanView
from pages.ProfileView import ProfileView
from pages.SettingsView import SettingsView

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CalorieMate - Homepage")
        self.geometry("1280x720")

        self.frames = {}  # Dictionary to store all pages
        self.container = tk.Frame(self)
        self.container.grid(row=0, column=0, sticky="nsew")

        self.initialize_pages()  # Initialize all pages

        self.show_page("HomePage")  # Default page to show (HomePage)

        # Configure grid layout to make the container expand properly
        self.grid_rowconfigure(0, weight=1)  # The row where the container is placed
        self.grid_columnconfigure(0, weight=1)  # The column where the container is placed

        self.create_buttons()  # Create buttons that will be free (not in navbar)

    def create_buttons(self):
        # Create navigation buttons directly in the main frame
        plan_button = tk.Button(self, text="Go to Plan View", command=lambda: self.show_page("PlanView"))
        plan_button.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        food_button = tk.Button(self, text="Go to Food View", command=lambda: self.show_page("FoodView"))
        food_button.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        # Configure grid for free buttons (2 buttons in this case)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def initialize_pages(self):
        # Initialize all pages but don't display them yet
        self.frames["HomePage"] = HomePage(parent=self.container, controller=self)
        self.frames["PlanView"] = PlanView(parent=self.container, controller=self)
        self.frames["FoodView"] = FoodView(parent=self.container, controller=self)
        self.frames["MakeFoodView"] = MakeFood(parent=self.container, controller=self)
        self.frames["MakePlanView"] = MakePlanView(parent=self.container, controller=self)

    def show_page(self, page_name):
        # Hide all frames
        for frame in self.frames.values():
            frame.grid_forget()

        # Show the selected page
        frame = self.frames[page_name]
        frame.grid(row=0, column=0, sticky="nsew")

        # Call load_foods() if we are showing the FoodView
        if page_name == "FoodView":
            frame.load_foods()  # Load foods when FoodView is displayed

        # Refresh PlanView when switching to it
        if page_name == "PlanView":
            frame.create_widgets()  # Refresh the plan list on load

        # Update the UI to reflect the changes
        self.update()

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        title_label = tk.Label(self, text="Welcome to CalorieMate!", font=("Helvetica", 24))
        title_label.grid(row=0, column=0, pady=20, padx=20, sticky="nsew")

        # Center the title label in the entire frame
        self.grid_rowconfigure(0, weight=1)  # Make the first row expand
        self.grid_columnconfigure(0, weight=1)  # Make the first column expand
        title_label.grid_configure(sticky="nsew")  # Center the label in the grid

        # Add more widgets to customize the homepage here
        # You can add buttons or other labels that will also be centered

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
