# src/logic/notifikasi.py
import sqlite3
from datetime import date
import os
import platform

class NotificationChecker:
    def __init__(self, db_path='src/database/database.db'):
        self.db_path = db_path

    def check_daily_calorie_intake(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        today = date.today().isoformat()

        cursor.execute('''
            SELECT calorie_budget, notification_enabled
            FROM UserPreference
            WHERE user_id = 1
        ''')
        user_preference = cursor.fetchone()

        if user_preference:
            calorie_budget, notification_enabled = user_preference

            cursor.execute('''
                SELECT total_calories
                FROM UserPlan
                WHERE date = ? AND eaten = 1
            ''', (today,))
            plans = cursor.fetchall()

            total_calories_consumed = sum(plan[0] for plan in plans)

            if total_calories_consumed > calorie_budget and notification_enabled:
                self.send_notification(total_calories_consumed, calorie_budget)

        conn.close()

    def send_notification(self, consumed, budget):
        title = 'Melebihi Limit Calories'
        message = f"Fat Alert!!! Kamu sudah mengonsumsi {consumed} calories hari ini, melebihi budget kamu: {budget} calories."

        system_platform = platform.system()

        if system_platform == "Windows":
            self.send_windows_notification(title, message)
        elif system_platform == "Darwin":
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

    def send_mac_notification(self, title, message):
        os.system(f"osascript -e 'display notification \"{message}\" with title \"{title}\"'")

    def send_linux_notification(self, title, message):
        os.system(f'notify-send "{title}" "{message}"')
