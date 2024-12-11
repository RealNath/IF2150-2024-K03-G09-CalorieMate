# src/logic/calorieCalculator.py
import sqlite3

class CalorieCalculator:
    def __init__(self, db_path='database.db'):
        self.db_path = db_path

    def calculate_daily_nutrition(self, date):
        # Connect to the SQLite database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Fetch all plans for the specified date from UserPlan
        cursor.execute('''
            SELECT plan_name, meal_type, total_calories, eaten
            FROM UserPlan
            WHERE date = ?
        ''', (date,))
        plans = cursor.fetchall()

        # Initialize totals
        total_calories = 0
        total_nutrition = {
            'protein': 0,
            'carbs': 0,
            'total_fat': 0,
            'cholesterol': 0,
            'saturated_fat': 0,
            'sodium': 0,
            'fiber': 0,
            'sugar': 0
        }
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
