# src/logic/calorieCalculator.py
import sqlite3

class CalorieCalculator:
    def __init__(self, db_path='database.db'):
        self.db_path = db_path

    def calculate_daily_nutrition(self, date):
        # Existing method...
        pass

    def calculate_total_calories_for_foods(self, food_list):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        total_calories = 0

        for food in food_list:
            cursor.execute('''
                SELECT calories
                FROM FoodDatabase
                WHERE name = ?
            ''', (food,))
            result = cursor.fetchone()
            if result:
                total_calories += result[0]

        conn.close()
        return total_calories
