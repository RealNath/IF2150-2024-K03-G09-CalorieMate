# src/main.py
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar as TkCalendar
import math
import importlib
import json
import datetime

# Importing Pages
from pages.PlanView import PlanView
from pages.HistoryView import HistoryView
from pages.ArticleView import ArticleView
from pages.FoodView import FoodView
from pages.ProfileView import ProfileView
from pages.SettingsView import SettingsView
from pages.MakePlanView import MakePlanView
from pages.MakeFoodView import MakeFoodView

# Other Imports
from logic.calorieCalculator import CalorieCalculator
from logic.DatabaseManager import DatabaseManager

from config import (
    COLOR_PRIMARY,
    COLOR_SECONDARY,
    COLOR_ACCENT,
    COLOR_BACKGROUND,
    COLOR_TEXT
)

Database = 'src/database/database.db'
db = DatabaseManager(Database)

def configure_styles():
    style = ttk.Style()
    style.theme_use('clam')

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


class NavMain(ttk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(style='NavMain.TFrame')
        self.controller = controller

        for item in controller.nav_main_items:
            btn_text = f"{item['icon']} {item['title']}"

            if 'badge' in item:
                btn_text += f"  {item['badge']}"

            if item['title'] == "Home":
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
                btn.state(['disabled'])

    def navigate(self, url):
        print(f"Navigating to {url}")


class UserInfo(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(style='UserInfo.TFrame')

        user = {
            "name": "Thor Odinson",
            "avatar": None,
        }

        avatar_label = ttk.Label(self, text="👤", font=("Arial", 24), background=COLOR_PRIMARY)
        avatar_label.pack(pady=(10, 5))

        name_label = ttk.Label(self, text=user["name"], style='UserInfo.TLabel')
        name_label.pack()


class CalendarWidget(ttk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.controller = controller
        self.calendar = TkCalendar(self, selectmode='day', date_pattern='yyyy-mm-dd')
        self.calendar.pack(pady=10, padx=10)

        self.calendar.bind("<<CalendarSelected>>", self.on_date_selected)

    def on_date_selected(self, event):
        selected_date = self.calendar.get_date()
        self.controller.update_selected_date(selected_date)


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
        self.show_page("PlanView")

    def show_page(self, page_name):
        if self.current_page:
            self.current_page.destroy()

        page_module = importlib.import_module(f"pages.{page_name}")
        page_class = getattr(page_module, page_name)
        self.current_page = page_class(self.container, self.controller)
        self.current_page.pack(fill="both", expand=True)


class SidebarLeft(ttk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        super().__init__(parent, width=200, *args, **kwargs)
        self.configure(style='SidebarLeft.TFrame')
        self.pack_propagate(False)
        self.pack(side="left", fill="y")

        container = ttk.Frame(self, style='SidebarLeft.TFrame')
        container.pack(expand=True)

        nav_main = NavMain(container, controller)
        nav_main.pack()


class SidebarRight(ttk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        super().__init__(parent, width=200, *args, **kwargs)
        self.configure(style='SidebarRight.TFrame')
        self.pack_propagate(False)
        self.pack(side="right", fill="y")

        user_info = UserInfo(self)
        user_info.pack(pady=10)

        calendar = CalendarWidget(self, controller)
        calendar.pack(pady=10, padx=10, fill="x")


class Dashboard(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.controller = self  # Dashboard acts as its own controller
        self.db_manager = db
        self.calorie_calculator = CalorieCalculator(db_manager=db)

        # Navigation Items
        self.nav_main_items = [
            {"title": "Home", "icon": "🏠", "url": "#"},
            {"title": "History", "icon": "📜", "url": "#"},
            {"title": "Article", "icon": "✨", "url": "#"},
            {"title": "Foods", "icon": "🍔", "url": "#"},
            {"title": "Settings", "icon": "⚙️", "url": "#"},
        ]

        self.sidebar_left = SidebarLeft(self, controller=self)
        self.sidebar_right = SidebarRight(self, controller=self)
        self.main_content = MainContent(self, controller=self)
        self.main_content.pack(fill="both", expand=True)
        self.pack(fill="both", expand=True)

    def show_page(self, page_name):
        self.main_content.show_page(page_name)

    def update_selected_date(self, selected_date):
        if hasattr(self.main_content.current_page, 'selected_date'):
            self.main_content.current_page.selected_date = selected_date
            if hasattr(self.main_content.current_page, 'load_plans'):
                self.main_content.current_page.load_plans()

    def enable_dark_mode(self):
        pass

    def disable_dark_mode(self):
        pass


def main():
    root = tk.Tk()
    root.title("Tkinter Dashboard Example")
    root.geometry("1200x800")

    configure_styles()
    dashboard = Dashboard(root)
    root.mainloop()

if __name__ == "__main__":
    main()
