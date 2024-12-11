# src/logic/calorieCalculator.py
from logic.DatabaseManager import DatabaseManager
import sqlite3
import json

class CalorieCalculator:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.db_path = db_manager.db_path

    def calculate_daily_nutrition(self, date):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # Fetch all plans for the specified date
        plans = self.db_manager.read(
            table="UserPlan",
            columns=["plan_name", "meal_type", "total_calories", "eaten"],
            conditions={"date": date},
            single=False
        )

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

        for plan in plans:
            plan_name, meal_type, plan_calories, eaten = plan
            cursor.execute('SELECT food_items FROM PlanDatabase WHERE plan_name = ?', (plan_name,))
            food_items_result = cursor.fetchone()

            if food_items_result:
                try:
                    food_items = json.loads(food_items_result[0])
                except:
                    food_items = eval(food_items_result[0])

                for food in food_items:
                    cursor.execute('''
                        SELECT calories, protein, carbs, total_fat, cholesterol, saturated_fat, sodium, fiber, sugar
                        FROM FoodDatabase
                        WHERE name = ?
                    ''', (food,))
                    food_data = cursor.fetchone()
                    if food_data:
                        cals, p, c, fat, chol, satfat, sod, fib, sug = food_data
                        total_calories += cals
                        total_nutrition['protein'] += p
                        total_nutrition['carbs'] += c
                        total_nutrition['total_fat'] += fat
                        total_nutrition['cholesterol'] += chol
                        total_nutrition['saturated_fat'] += satfat
                        total_nutrition['sodium'] += sod
                        total_nutrition['fiber'] += fib
                        total_nutrition['sugar'] += sug

        conn.close()
        return total_calories, total_nutrition

    def calculate_total_calories_for_foods(self, food_list):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        total_calories = 0
        for food in food_list:
            cursor.execute('SELECT calories FROM FoodDatabase WHERE name = ?', (food,))
            result = cursor.fetchone()
            if result:
                total_calories += result[0]
        conn.close()
        return total_calories
