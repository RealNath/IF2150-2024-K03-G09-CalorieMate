# src/main.py
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar as TkCalendar
import importlib
from PIL import Image, ImageTk
import datetime
from datetime import date
import os

# Importing Pages
from pages.PlanView import PlanView
from pages.HistoryView import HistoryView
from pages.ArticleView import ArticleView
from pages.FoodView import FoodView
from pages.ProfileView import ProfileView
from pages.SettingsView import SettingsView
from pages.MakePlanView import MakePlanView
from pages.MakeFoodView import MakeFoodView
from pages.editFood import EditFoodView

# Imporing Logic
from logic.calorieCalculator import CalorieCalculator
from logic.DatabaseManager import DatabaseManager
from logic.notifikasi import NotificationChecker

from config import (
    COLOR_PRIMARY,
    COLOR_SECONDARY,
    COLOR_ACCENT,
    COLOR_BACKGROUND,
    COLOR_TEXT,
    DARK_COLOR_PRIMARY,
    DARK_COLOR_SECONDARY,
    DARK_COLOR_ACCENT,
    DARK_COLOR_BACKGROUND,
    DARK_COLOR_TEXT
)

Database = 'src/database/database.db'
db = DatabaseManager(Database)


class ThemeManager:
    def __init__(self):
        # Store mode in memory for quick access
        self.dark_mode = False
        self.load_mode_from_db()

    def load_mode_from_db(self):
        db.connect()
        mode = db.read("UserPreference", ["DarkMode"], {"user_id": 1}, True)
        db.disconnect()
        if mode and mode[0] == 1:
            self.dark_mode = True
        else:
            self.dark_mode = False

    def get_colors(self):
        if self.dark_mode:
            return (
                DARK_COLOR_PRIMARY,
                DARK_COLOR_SECONDARY,
                DARK_COLOR_ACCENT,
                DARK_COLOR_BACKGROUND,
                DARK_COLOR_TEXT
            )
        else:
            return (
                COLOR_PRIMARY,
                COLOR_SECONDARY,
                COLOR_ACCENT,
                COLOR_BACKGROUND,
                COLOR_TEXT
            )


theme_manager = ThemeManager()
(CURR_COLOR_PRIMARY,
 CURR_COLOR_SECONDARY,
 CURR_COLOR_ACCENT,
 CURR_COLOR_BACKGROUND,
 CURR_COLOR_TEXT) = theme_manager.get_colors()


def configure_styles():
    style = ttk.Style()
    style.theme_use('clam')

    # Sidebar Left Styles
    style.configure('SidebarLeft.TFrame', background=CURR_COLOR_PRIMARY)
    style.configure('NavMain.TFrame', background=CURR_COLOR_PRIMARY)
    style.configure('NavMain.TButton',
                    foreground=CURR_COLOR_TEXT,
                    background=CURR_COLOR_SECONDARY,
                    relief="flat",
                    font=("Roboto", 12, "bold"),
                    padding=10)
    style.map('NavMain.TButton',
              background=[('active', CURR_COLOR_ACCENT)],
              foreground=[('active', CURR_COLOR_TEXT)])

    # Sidebar Right Styles
    style.configure('SidebarRight.TFrame', background=CURR_COLOR_PRIMARY)
    style.configure('SidebarRight.TLabel',
                    background=CURR_COLOR_PRIMARY,
                    foreground=CURR_COLOR_TEXT,
                    font=("Roboto", 14, "bold"))
    style.configure('SidebarRight.TButton',
                    foreground=CURR_COLOR_TEXT,
                    background=CURR_COLOR_SECONDARY,
                    relief="flat",
                    font=("Roboto", 12, "bold"),
                    padding=10)
    style.map('SidebarRight.TButton',
              background=[('active', CURR_COLOR_ACCENT)],
              foreground=[('active', CURR_COLOR_TEXT)])

    # Main Content Styles
    style.configure('MainContent.TFrame', background=CURR_COLOR_BACKGROUND)
    style.configure('MainContent.TLabel',
                    background=CURR_COLOR_BACKGROUND,
                    foreground=CURR_COLOR_PRIMARY,
                    font=("Roboto", 16, "bold"))
    style.configure('Header.TFrame', background=CURR_COLOR_BACKGROUND)
    style.configure('Header.TLabel',
                    background=CURR_COLOR_BACKGROUND,
                    foreground=CURR_COLOR_PRIMARY,
                    font=("Roboto", 16, "bold"))
    style.configure('Badge.TLabel',
                    background="#e74c3c",
                    foreground=CURR_COLOR_TEXT,
                    font=("Roboto", 8, "bold"))

    # User Info Styles
    style.configure('UserInfo.TFrame', background=CURR_COLOR_PRIMARY)
    style.configure('UserInfo.TLabel',
                    background=CURR_COLOR_PRIMARY,
                    foreground=CURR_COLOR_TEXT,
                    font=("Roboto", 12, "bold"))

    # Separators
    style.configure('VerticalSeparator.TSeparator', orient='vertical')
    style.configure('HorizontalSeparator.TSeparator', orient='horizontal')

    # Progressbar style
    style.configure('TProgressbar', troughcolor=CURR_COLOR_PRIMARY, background=CURR_COLOR_ACCENT)


class NavMain(ttk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.controller = controller
        self.configure(style='NavMain.TFrame')

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
        self.user = {}
        self.avatar_label = None
        self.name_label = None
        self.load_user_info()

    def load_user_info(self):
        for widget in self.winfo_children():
            widget.destroy()

        db.connect()
        user_data = db.read("UserPreference", ["name", "profile_image"], {"user_id": 1}, True)
        db.disconnect()

        if user_data:
            self.user["name"] = user_data[0]
            self.user["avatar"] = user_data[1]
        else:
            self.user["name"] = "Default User"
            self.user["avatar"] = None

        if self.user["avatar"] and self.user["avatar"] != "":
            try:
                img = Image.open(self.user["avatar"])
                img = img.resize((80, 80), Image.ANTIALIAS)
                self.user_photo = ImageTk.PhotoImage(img)
                self.avatar_label = ttk.Label(self, image=self.user_photo, background=CURR_COLOR_PRIMARY)
            except:
                # If image fails to load, fallback to default text avatar
                self.avatar_label = ttk.Label(self, text="👤", font=("Roboto", 24), background=CURR_COLOR_PRIMARY)
        else:
            self.avatar_label = ttk.Label(self, text="👤", font=("Roboto", 24), background=CURR_COLOR_PRIMARY)

        self.avatar_label.pack(pady=(10, 5))
        self.name_label = ttk.Label(self, text=self.user["name"], style='UserInfo.TLabel')
        self.name_label.pack()


class CalendarWidget(ttk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.controller = controller
        self.calendar = TkCalendar(self, selectmode='day', date_pattern='yyyy-mm-dd')
        self.calendar.pack(pady=10, padx=10)

        self.calendar.bind("<<CalendarSelected>>", self.on_date_selected)

    def on_date_selected(self, event):
        selected_date = self.calendar.get_date()
        self.controller.selected_date = selected_date
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

    def show_page(self, page_name, **kwargs):
        if self.current_page:
            self.current_page.destroy()
        page_module = importlib.import_module(f"pages.{page_name.split('.')[0]}")
        page_class = getattr(page_module, page_name.split('.')[-1])
        self.current_page = page_class(self.container, self.controller, **kwargs)
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

        self.controller = controller

        self.user_info = UserInfo(self)
        self.user_info.pack(pady=10)

        calendar = CalendarWidget(self, controller)
        calendar.pack(pady=10, padx=10, fill="x")

        ttk.Label(self, text="Calorie Meter", style='SidebarRight.TLabel').pack(pady=10)
        self.calorie_bar = ttk.Progressbar(self, orient="horizontal", length=150, mode='determinate')
        self.calorie_bar.pack(pady=5, padx=10)

        self.calorie_label = ttk.Label(self, text="", style='SidebarRight.TLabel')
        self.calorie_label.pack()

        self.update_calorie_meter()

    def update_calorie_meter(self):
        db.connect()
        pref = db.read("UserPreference", ["calorie_budget", "notification_enabled"], {"user_id": 1}, True)
        db.disconnect()

        if pref:
            calorie_budget, notification_enabled = pref
        else:
            calorie_budget, notification_enabled = 2000, 0

        today = self.controller.selected_date
        db.connect()
        eaten_plans = db.read("UserPlan", ["total_calories"], {"date": today, "eaten": 1}, False)
        db.disconnect()

        total_consumed = sum(p[0] for p in eaten_plans) if eaten_plans else 0

        self.calorie_bar["maximum"] = calorie_budget
        self.calorie_bar["value"] = total_consumed
        self.calorie_label.config(text=f"{total_consumed}/{calorie_budget} kcal")

        # Change bar color if exceeded
        s = ttk.Style()
        if total_consumed > calorie_budget:
            s.configure('TProgressbar', background='red', troughcolor=CURR_COLOR_PRIMARY)
        else:
            s.configure('TProgressbar', background=CURR_COLOR_ACCENT, troughcolor=CURR_COLOR_PRIMARY)

        # Immediate notification if exceeded
        if total_consumed > calorie_budget and notification_enabled:
            notifier = NotificationChecker()
            notifier.check_daily_calorie_intake()


class Dashboard(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.controller = self  # Dashboard acts as its own controller
        self.db_manager = db
        self.calorie_calculator = CalorieCalculator(db_manager=db)
        self.selected_date = date.today().isoformat()  # Store a default selected date

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

    def show_page(self, page_name, **kwargs):
        self.main_content.show_page(page_name, **kwargs)

    def update_selected_date(self, selected_date):
        self.selected_date = selected_date
        if hasattr(self.main_content.current_page, 'selected_date'):
            self.main_content.current_page.selected_date = selected_date
            if hasattr(self.main_content.current_page, 'load_plans'):
                self.main_content.current_page.load_plans()

        self.sidebar_right.update_calorie_meter()

    def enable_dark_mode(self):
        # Update DB
        db.connect()
        db.update("UserPreference", {"DarkMode": 1}, {"user_id": 1})
        db.disconnect()
        self.reload_theme()

    def disable_dark_mode(self):
        db.connect()
        db.update("UserPreference", {"DarkMode": 0}, {"user_id": 1})
        db.disconnect()
        self.reload_theme()

    def reload_theme(self):
        # Reload mode from DB and re-configure styles
        theme_manager.load_mode_from_db()
        global CURR_COLOR_PRIMARY, CURR_COLOR_SECONDARY, CURR_COLOR_ACCENT, CURR_COLOR_BACKGROUND, CURR_COLOR_TEXT
        (CURR_COLOR_PRIMARY,
         CURR_COLOR_SECONDARY,
         CURR_COLOR_ACCENT,
         CURR_COLOR_BACKGROUND,
         CURR_COLOR_TEXT) = theme_manager.get_colors()
        configure_styles()

        # Force refresh current UI
        # Re-initialize?
        # The simplest way is to destroy all and rebuild the dashboard,
        # but let's just refresh pages and sidebars:
        self.sidebar_left.destroy()
        self.sidebar_right.destroy()
        self.main_content.destroy()

        self.sidebar_left = SidebarLeft(self, controller=self)
        self.sidebar_right = SidebarRight(self, controller=self)
        self.main_content = MainContent(self, controller=self)
        self.main_content.pack(fill="both", expand=True)


def main():
    root = tk.Tk()
    root.title("CalorieMate")
    root.geometry("1200x800")

    configure_styles()
    dashboard = Dashboard(root)
    root.mainloop()

if __name__ == "__main__":
    main()
