# src/main.py
import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar as TkCalendar
import math
import importlib

# Importing Pages
from pages.PlanView import PlanView
from pages.HistoryView import HistoryView
from pages.ArticleView import ArticleView
from pages.FoodView import FoodView
from pages.ProfileView import ProfileView
from pages.SettingsView import SettingsView

# Other Imports
from logic.calorieCalculator import CalorieCalculator

# Import color constants from config.py
from config import (
    COLOR_PRIMARY,
    COLOR_SECONDARY,
    COLOR_ACCENT,
    COLOR_BACKGROUND,
    COLOR_TEXT
)

# ---------------------------
# Style Configuration
# ---------------------------
def configure_styles():
    style = ttk.Style()
    style.theme_use('clam')  # Choose a base theme

    # Sidebar Left Styles
    style.configure('SidebarLeft.TFrame', background=COLOR_PRIMARY)
    
    style.configure('NavMain.TFrame', background=COLOR_PRIMARY)
    
    style.configure('NavMain.TButton',
                    foreground=COLOR_TEXT,
                    background=COLOR_SECONDARY,
                    relief="flat",
                    font=("Arial", 12, "bold"),
                    padding=10)
    
    style.map('NavMain.TButton',
              background=[('active', COLOR_ACCENT)],
              foreground=[('active', COLOR_TEXT)])
    
    # Sidebar Right Styles
    style.configure('SidebarRight.TFrame', background=COLOR_PRIMARY)
    style.configure('SidebarRight.TLabel',
                    background=COLOR_PRIMARY,
                    foreground=COLOR_TEXT,
                    font=("Arial", 14, "bold"))
    style.configure('SidebarRight.TButton',
                    foreground=COLOR_TEXT,
                    background=COLOR_SECONDARY,
                    relief="flat",
                    font=("Arial", 12, "bold"),
                    padding=10)
    style.map('SidebarRight.TButton',
              background=[('active', COLOR_ACCENT)],
              foreground=[('active', COLOR_TEXT)])
    
    # Main Content Styles
    style.configure('MainContent.TFrame', background=COLOR_BACKGROUND)
    style.configure('MainContent.TLabel',
                    background=COLOR_BACKGROUND,
                    foreground=COLOR_PRIMARY,
                    font=("Arial", 16, "bold"))
    style.configure('Header.TFrame', background=COLOR_BACKGROUND)
    style.configure('Header.TLabel',
                    background=COLOR_BACKGROUND,
                    foreground=COLOR_PRIMARY,
                    font=("Arial", 16, "bold"))
    style.configure('Badge.TLabel',
                    background="#e74c3c",
                    foreground=COLOR_TEXT,
                    font=("Arial", 8, "bold"))
    
    # User Info Styles
    style.configure('UserInfo.TFrame', background=COLOR_PRIMARY)
    style.configure('UserInfo.TLabel',
                    background=COLOR_PRIMARY,
                    foreground=COLOR_TEXT,
                    font=("Arial", 12, "bold"))
    
    # Separator Style
    style.configure('VerticalSeparator.TSeparator', orient='vertical')
    style.configure('HorizontalSeparator.TSeparator', orient='horizontal')

# ---------------------------
# Make Plan Pop-up Widget
# ---------------------------
class MakePlanPopup(tk.Toplevel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.title("Make a Plan")
        self.geometry("400x300")  # Width x Height
        self.configure(bg=COLOR_BACKGROUND)
        
        # Make the pop-up modal
        self.transient(parent)
        self.grab_set()
        
        # Example Widgets in Pop-up
        label = ttk.Label(self, text="Create a New Plan", font=("Arial", 16, "bold"), background=COLOR_BACKGROUND)
        label.pack(pady=20)

        # Plan Title Entry
        title_label = ttk.Label(self, text="Plan Title:", background=COLOR_BACKGROUND, font=("Arial", 12))
        title_label.pack(pady=(10, 5), padx=20, anchor='w')
        self.title_entry = ttk.Entry(self)
        self.title_entry.pack(pady=(0, 10), padx=20, fill='x')

        # Plan Description Text
        desc_label = ttk.Label(self, text="Description:", background=COLOR_BACKGROUND, font=("Arial", 12))
        desc_label.pack(pady=(10, 5), padx=20, anchor='w')
        self.desc_text = tk.Text(self, height=5, wrap='word')
        self.desc_text.pack(pady=(0, 10), padx=20, fill='both', expand=True)

        # Save Button
        save_button = ttk.Button(self, text="Save Plan", command=self.save_plan)
        save_button.pack(pady=10)

    def save_plan(self):
        title = self.title_entry.get().strip()
        description = self.desc_text.get("1.0", tk.END).strip()
        
        if title:
            print(f"Plan Saved!\nTitle: {title}\nDescription: {description}")
            self.destroy()
        else:
            print("Please enter a plan title.")

# ---------------------------
# Navigation Main Component
# ---------------------------
class NavMain(ttk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(style='NavMain.TFrame')
        self.controller = controller

        for item in controller.nav_main_items:
            btn_text = f"{item['icon']} {item['title']}"
            if 'badge' in item:
                btn_text += f"  {item['badge']}"
            
            # Assign specific commands based on title
            if item['title'] == "Make Plan":
                btn = ttk.Button(self, text=btn_text, style='NavMain.TButton',
                                 command=lambda: controller.show_page("PlanView"))
            elif item['title'] == "Home":
                btn = ttk.Button(self, text=btn_text, style='NavMain.TButton',
                                 command=lambda: controller.show_page("PlanView"))
            elif item['title'] == "History":
                btn = ttk.Button(self, text=btn_text, style='NavMain.TButton',
                                 command=lambda: controller.show_page("HistoryView"))
            elif item['title'] == "Article":
                btn = ttk.Button(self, text=btn_text, style='NavMain.TButton',
                                 command=lambda: controller.show_page("ArticleView"))
            elif item['title'] == "Foods":
                btn = ttk.Button(self, text=btn_text, style='NavMain.TButton',
                                 command=lambda: controller.show_page("FoodView"))
            elif item['title'] == "Settings":
                btn = ttk.Button(self, text=btn_text, style='NavMain.TButton',
                                 command=lambda: controller.show_page("SettingsView"))
            else:
                btn = ttk.Button(self, text=btn_text, style='NavMain.TButton',
                                 command=lambda url=item['url']: self.navigate(url))
            
            btn.pack(fill="x", pady=5, padx=20)

            if item.get('isActive'):
                btn.state(['disabled'])  # Indicate active button

    def navigate(self, url):
        print(f"Navigating to {url}")

# ---------------------------
# User Info Component
# ---------------------------
class UserInfo(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(style='UserInfo.TFrame')

        # Example User Data
        user = {
            "name": "Thor Odinson",
            "avatar": None,
        }

        # Avatar (Using Emoji as Placeholder)
        avatar_label = ttk.Label(self, text="👤", font=("Arial", 24), background=COLOR_PRIMARY)
        avatar_label.pack(pady=(10, 5))

        # User Name
        name_label = ttk.Label(self, text=user["name"], style='UserInfo.TLabel')
        name_label.pack()

# ---------------------------
# Calendar Component
# ---------------------------
class CalendarWidget(ttk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.controller = controller
        self.calendar = TkCalendar(self, selectmode='day')
        self.calendar.pack(pady=10, padx=10)

        # Bind date selection
        self.calendar.bind("<<CalendarSelected>>", self.on_date_selected)

    def on_date_selected(self, event):
        selected_date = self.calendar.get_date()
        print(f"Selected date: {selected_date}")
        self.controller.update_selected_date(selected_date)

    def update_value(self, new_value):
        if new_value > self.max_value:
            new_value = self.max_value
        elif new_value < 0:
            new_value = 0
        self.current_value = new_value

        angle = 180 - (self.current_value / self.max_value) * 180
        x_end = 100 + 80 * math.cos(math.radians(angle))
        y_end = 100 - 80 * math.sin(math.radians(angle))

        # Update needle position
        self.canvas.coords(self.needle, 100, 100, x_end, y_end)

# ---------------------------
# Main Content Component
# ---------------------------
class MainContent(ttk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(style='MainContent.TFrame')
        self.controller = controller
        self.current_page = None
        self.create_widgets()

    def create_widgets(self):
        self.container = ttk.Frame(self, style='MainContent.TFrame')
        self.container.pack(fill="both", expand=True)
        self.show_page("PlanView")  # Default page

    def show_page(self, page_name):
        if self.current_page:
            self.current_page.destroy()
        
        page_class = getattr(importlib.import_module(f"pages.{page_name}"), page_name)
        self.current_page = page_class(self.container, self.controller)
        self.current_page.pack(fill="both", expand=True)

# ---------------------------
# Sidebar Left Component
# ---------------------------
class SidebarLeft(ttk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        super().__init__(parent, width=200, *args, **kwargs)
        self.configure(style='SidebarLeft.TFrame')
        self.pack_propagate(False)  # Prevent frame from resizing to fit its contents
        self.pack(side="left", fill="y")

        # Container frame to center navigation buttons vertically
        container = ttk.Frame(self, style='SidebarLeft.TFrame')
        container.pack(expand=True)

        # Main Navigation
        nav_main = NavMain(container, controller)
        nav_main.pack()

    def switch_team(self, team_name):
        print(f"Switched to team: {team_name}")

# ---------------------------
# Sidebar Right Component
# ---------------------------
class SidebarRight(ttk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        super().__init__(parent, width=200, *args, **kwargs)
        self.configure(style='SidebarRight.TFrame')
        self.pack_propagate(False)  # Prevent frame from resizing to fit its contents
        self.pack(side="right", fill="y")

        # User Info
        user_info = UserInfo(self)
        user_info.pack(pady=10)

        # Calendar
        calendar = CalendarWidget(self, controller)
        calendar.pack(pady=10, padx=10, fill="x")

# ---------------------------
# Dashboard Component
# ---------------------------
class Dashboard(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.pack(fill="both", expand=True)

        # Initialize Calorie Calculator
        self.calorie_calculator = CalorieCalculator(db_path='src/database/database.db')

        # Navigation Items
        self.nav_main_items = [
            {"title": "Home", "icon": "🏠", "url": "#", "isActive": True},
            {"title": "History", "icon": "📜", "url": "#"},
            {"title": "Article", "icon": "✨", "url": "#"},
            {"title": "Foods", "icon": "🍔", "url": "#"},
            {"title": "Settings", "icon": "⚙️", "url": "#"},
        ]

        # Initialize Sidebars
        self.sidebar_left = SidebarLeft(self, controller=self)
        self.sidebar_right = SidebarRight(self, controller=self)

        # Main Content Area
        self.main_content = MainContent(self, controller=self)
        self.main_content.pack(fill="both", expand=True)

    def show_page(self, page_name):
        self.main_content.show_page(page_name)

    def update_selected_date(self, selected_date):
        # Broadcast the selected date to relevant pages
        print(f"Dashboard received selected date: {selected_date}")
        if hasattr(self.main_content.current_page, 'selected_date'):
            self.main_content.current_page.selected_date = selected_date
            self.main_content.current_page.plan_name_entry.config(state='normal')
            self.main_content.current_page.plan_name_entry.delete(0, tk.END)
            self.main_content.current_page.meal_type_var.set("breakfast")
            self.main_content.current_page.foods_listbox.delete(0, tk.END)
            self.main_content.current_page.selected_foods = []
            self.main_content.current_page.save_plan()  # Refresh the plan

    def enable_dark_mode(self):
        # Implement dark mode if desired
        pass

    def disable_dark_mode(self):
        # Implement disable dark mode if desired
        pass

# ---------------------------
# Application Entry Point
# ---------------------------
def main():
    root = tk.Tk()
    root.title("Tkinter Dashboard Example")
    root.geometry("1200x800")  # Width x Height

    # Configure Styles
    configure_styles()

    # Initialize Dashboard
    dashboard = Dashboard(root)

    root.mainloop()

if __name__ == "__main__":
    main()
