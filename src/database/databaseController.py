import sqlite3

conn = sqlite3.connect('src/database/database.db')
cursor = conn.cursor()

# UserPreference table
cursor.execute('''
    CREATE TABLE UserPreference (
        user_id INTEGER PRIMARY KEY,
        name TEXT,
        calorie_budget INTEGER,
        weight_goal TEXT,
        notification_enabled BOOLEAN,
        DarkMode BOOLEAN
    )
''')
cursor.execute('''
    INSERT INTO UserPreference (user_id, name, calorie_budget, weight_goal, notification_enabled, DarkMode)
    VALUES (1, 'User', 2000, 'maintain', 1, 1)
''')

# ArticleDatabase table
cursor.execute('''
    CREATE TABLE ArticleDatabase (
        article_id INTEGER PRIMARY KEY,
        article_name TEXT,
        article_author TEXT,
        text TEXT
    )
''')
cursor.execute('''
    INSERT INTO ArticleDatabase (article_id, article_name, article_author, text)
    VALUES (1, 'Healthy Eating', 'Dr Bendover', 'Healthy eating is about maintaining a balanced diet. It involves consuming a variety of foods to get essential nutrients, including proteins, carbs, fats, vitamins, and minerals. It''s important to find a good balance between energy intake and physical activity for maintaining a healthy lifestyle.')
''')

# FoodDatabase table
cursor.execute('''
    CREATE TABLE FoodDatabase (
        food_id INTEGER PRIMARY KEY,
        name TEXT,
        calories INTEGER,
        protein REAL,
        carbs REAL,
        total_fat REAL,
        cholesterol REAL,
        saturated_fat REAL,
        sodium REAL,
        fiber REAL,
        sugar REAL,
        other_nutrients TEXT
    )
''')
cursor.execute('''
    INSERT INTO FoodDatabase (food_id, name, calories, protein, carbs, total_fat, cholesterol, saturated_fat, sodium, fiber, sugar, other_nutrients)
    VALUES (1, 'chicken breast', 200, 30, 0, 5, 0, 1, 0.16, 3, 4, '{"vitaminB6": 0.5, "iron": 1.2}')
''')

# UserPlan table
cursor.execute('''
    CREATE TABLE UserPlan (
        plan_id INTEGER PRIMARY KEY,
        plan_name TEXT,
        date TEXT,
        meal_type TEXT,
        total_calories INTEGER,
        eaten BOOLEAN
    )
''')
cursor.execute('''
    INSERT INTO UserPlan (plan_id, plan_name, date, meal_type, total_calories, eaten)
    VALUES (1, 'generic_breakfast', '2024-12-04', 'breakfast', 500, 0)
''')

# PlanDatabase table
cursor.execute('''
    CREATE TABLE PlanDatabase (
        plan_id INTEGER PRIMARY KEY,
        plan_name TEXT,
        meal_type TEXT,
        food_items TEXT,
        total_calories INTEGER
    )
''')
cursor.execute('''
    INSERT INTO PlanDatabase (plan_id, plan_name, meal_type, food_items, total_calories)
    VALUES (1, 'generic_lunch', 'lunch', '["chicken breast", "rice", "broccoli"]', 600)
''')

conn.commit()
conn.close()
