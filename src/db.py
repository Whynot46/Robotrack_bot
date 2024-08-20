import sqlite3 as sql
import pandas as pd
import ast
from src.config import DB_PATH


def add_new_user(user_id, username, child_name, child_age, parent_number):
    connection = sql.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute('''
            INSERT INTO Users (user_id, username, child_name, child_age, parent_number)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, username, child_name, child_age, parent_number))
    connection.commit()


def add_lesson(date, time, topic, age):
    connection = sql.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute('''
            INSERT INTO Users (date, time, topic, age)
            VALUES (?, ?, ?, ?)
        ''', (date, time, topic, age))
    connection.commit()
    

def is_old(user_id):
    connection = sql.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("SELECT 1 FROM Users WHERE user_id = ?", (user_id,))
    result  = cursor.fetchone()
    connection.commit()
    return bool(result)


def get_users_data():
    connection = sql.connect(DB_PATH) 
    xlsx_file = pd.read_sql_query('SELECT user_id, username, child_name, child_age, parent_number FROM User', connection) 
    xlsx_file.to_excel("./db/users_data.xlsx", index=False)  
    connection.close() 


def get_lessons_data():
    connection = sql.connect(DB_PATH) 
    xlsx_file = pd.read_sql_query('SELECT date, time, topic, age FROM Lessons', connection) 
    xlsx_file.to_excel("./db/lessons_data.xlsx", index=False)  
    connection.close() 


def get_shedule_data():
    connection = sql.connect(DB_PATH) 
    xlsx_file = pd.read_sql_query('SELECT date, weekday, lessons FROM Shedule', connection) 
    xlsx_file.to_excel("./db/shedule_data.xlsx", index=False)  
    connection.close() 


def get_lessons(weekday : str) -> list: # list of tuple
    connection = sql.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("SELECT lessons FROM Shedule WHERE weekday = ?", (weekday,))
    results = cursor.fetchall()
    results = str(results[0])
    results = results[2:-3]
    lessons = ast.literal_eval(results)

    return lessons
