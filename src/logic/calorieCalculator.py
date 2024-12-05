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

        # Iterate over each plan to calculate total nutrition
        for plan in plans:
            plan_name, meal_type, plan_calories, eaten = plan

            cursor.execute('''
                SELECT food_items
                FROM PlanDatabase
                WHERE plan_name = ?
            ''', (plan_name,))
            food_items_result = cursor.fetchone()

            if food_items_result:
                food_items = eval(food_items_result[0])  # Convert string to  list

                for food in food_items:
                    cursor.execute('''
                        SELECT calories, protein, carbs, total_fat, cholesterol, saturated_fat, sodium, fiber, sugar
                        FROM FoodDatabase
                        WHERE name = ?
                    ''', (food,))
                    food_data = cursor.fetchone()

                    if food_data:
                        calories, protein, carbs, total_fat, cholesterol, saturated_fat, sodium, fiber, sugar = food_data
                        
                        total_calories += calories
                        total_nutrition['protein'] += protein
                        total_nutrition['carbs'] += carbs
                        total_nutrition['total_fat'] += total_fat
                        total_nutrition['cholesterol'] += cholesterol
                        total_nutrition['saturated_fat'] += saturated_fat
                        total_nutrition['sodium'] += sodium
                        total_nutrition['fiber'] += fiber
                        total_nutrition['sugar'] += sugar

        conn.close()

        return total_calories, total_nutrition