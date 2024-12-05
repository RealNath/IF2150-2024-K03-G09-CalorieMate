import sqlite3
from datetime import date
import os
import platform

class NotificationChecker:
    def __init__(self, db_path='database.db'):
        self.db_path = db_path

    def check_daily_calorie_intake(self):
        # Connect to the database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get the current date
        today = date.today().isoformat()

        # Get user preference for calorie budget and notification setting
        cursor.execute('''
            SELECT calorie_budget, notification_enabled
            FROM UserPreference
            WHERE user_id = 1
        ''')
        user_preference = cursor.fetchone()

        if user_preference:
            calorie_budget, notification_enabled = user_preference

            # Get all eaten plans for the current date
            cursor.execute('''
                SELECT total_calories
                FROM UserPlan
                WHERE date = ? AND eaten = 1
            ''', (today,))
            plans = cursor.fetchall()

            # Calculate total calories consumed for the day
            total_calories_consumed = sum(plan[0] for plan in plans)

            # Check if the calories consumed exceeds the budget and if notifications are enabled
            if total_calories_consumed > calorie_budget and notification_enabled:
                self.send_notification(total_calories_consumed, calorie_budget)

        conn.close()

    def send_notification(self, consumed, budget):
        title = 'Melebihi Limit Calories'
        message = f"Fat Alert!!! Kamu sudah mengonsumsi {consumed} calories hari ini, melebihi budget kamu: {budget} calories. Nanti gendut lagi loooh."
        system_platform = platform.system()

        if system_platform == "Windows":
            self.send_windows_notification(title, message)
        elif system_platform == "Darwin":  # macOS
            self.send_mac_notification(title, message)
        elif system_platform == "Linux":
            self.send_linux_notification(title, message)

    def send_windows_notification(self, title, message):
        command = f"""
        [reflection.assembly]::loadwithpartialname('System.Windows.Forms') | Out-Null;
        [reflection.assembly]::loadwithpartialname('System.Drawing') | Out-Null;
        $notify = new-object system.windows.forms.notifyicon;
        $notify.icon = [System.Drawing.SystemIcons]::Information;
        $notify.visible = $true;
        $notify.showballoontip(10, '{title}', '{message}', [system.windows.forms.tooltipicon]::None);
        """
        os.system(f"powershell -command \"{command}\"")
