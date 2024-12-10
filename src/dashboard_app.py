import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar as TkCalendar
import math

# ---------------------------
# Color Scheme Definitions
# ---------------------------
COLOR_PRIMARY = "#355F2E"      # Dark Green
COLOR_SECONDARY = "#A8CD89"    # Greenish
COLOR_ACCENT = "#F9C0AB"       # Light Orange/Pink
COLOR_BACKGROUND = "#F4E0AF"   # Light Yellowish
COLOR_TEXT = "#FFFFFF"         # White for text on dark backgrounds

# ---------------------------
# Sample Data Definitions
# ---------------------------
data = {
    "navMain": [
        {
            "title": "Home",
            "icon": "🏠",
            "url": "#",
            "isActive": True,
        },
        {
            "title": "Make Plan",
            "icon": "🔍",
            "url": "#",
        },
        {
            "title": "Article",
            "icon": "✨",
            "url": "#",
        },
        {
            "title": "Foods",
            "icon": "🍔",
            "url": "#",
        },
        {
            "title": "Settings",
            "icon": "⚙️",
            "url": "#",
        },
    ],
}

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
# Navigation Main Component
# ---------------------------
class NavMain(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(style='NavMain.TFrame')

        for item in data['navMain']:
            btn_text = f"{item['icon']} {item['title']}"
            if 'badge' in item:
                btn_text += f"  {item['badge']}"
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
            "avatar": None,  # Path to avatar image if available
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
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.calendar = TkCalendar(self, selectmode='day')
        self.calendar.pack(pady=10, padx=10)

        # Bind date selection
        self.calendar.bind("<<CalendarSelected>>", self.on_date_selected)

    def on_date_selected(self, event):
        selected_date = self.calendar.get_date()
        print(f"Selected date: {selected_date}")

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
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(style='MainContent.TFrame')

        # Header
        header = ttk.Frame(self, style='Header.TFrame', height=50)
        header.pack(fill="x")

        # Breadcrumb (Changed text and centered it)
        breadcrumb = ttk.Label(header, text="Plan for the day", style='Header.TLabel')
        breadcrumb.pack(expand=True)

        # Main Body
        body = ttk.Frame(self, style='MainContent.TFrame')
        body.pack(fill="both", expand=True, padx=10, pady=10)

        # Example Content Boxes
        box2 = ttk.Label(body, text="Content Box 2", background=COLOR_SECONDARY, relief="sunken", anchor="center",
                         font=("Arial", 12, "bold"))
        box2.pack(fill="both", expand=True, pady=5)

# ---------------------------
# Left Sidebar Component
# ---------------------------
class SidebarLeft(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, width=200, *args, **kwargs)
        self.configure(style='SidebarLeft.TFrame')
        self.pack_propagate(False)  # Prevent frame from resizing to fit its contents
        self.pack(side="left", fill="y")

        # Container frame to center navigation buttons vertically
        container = ttk.Frame(self, style='SidebarLeft.TFrame')
        container.pack(expand=True)

        # Main Navigation
        nav_main = NavMain(container)
        nav_main.pack()

    def switch_team(self, team_name):
        print(f"Switched to team: {team_name}")

# ---------------------------
# Right Sidebar Component
# ---------------------------
class SidebarRight(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, width=200, *args, **kwargs)
        self.configure(style='SidebarRight.TFrame')
        self.pack_propagate(False)  # Prevent frame from resizing to fit its contents
        self.pack(side="right", fill="y")

        # User Info
        user_info = UserInfo(self)
        user_info.pack(pady=10)

        # Calendar
        calendar = CalendarWidget(self)
        calendar.pack(pady=10, padx=10, fill="x")

# ---------------------------
# Dashboard Component
# ---------------------------
class Dashboard(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.pack(fill="both", expand=True)

        # Initialize Left and Right Sidebars
        self.sidebar_left = SidebarLeft(self)
        self.sidebar_right = SidebarRight(self)

        # Main Content Area
        self.main_content = MainContent(self)
        self.main_content.pack(fill="both", expand=True)

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
