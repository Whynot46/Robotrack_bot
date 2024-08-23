import sqlite3 as sql
import pandas as pd
import ast
from src.config import DB_PATH


def add_new_user(user_id, username, child_name, child_age, parent_number):
    connection = sql.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute('''
            INSERT INTO Users (user_id, username, child_name, child_birthday, parent_number)
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


def get_username(user_id):
    connection = sql.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("SELECT username FROM Users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    connection.commit()
    return result[0] if result else None


def get_child_name(user_id):
    connection = sql.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("SELECT child_name FROM Users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    connection.commit()
    return result[0] if result else None


def get_child_birthday(user_id):
    connection = sql.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("SELECT child_birthday FROM Users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    connection.commit()
    return result[0] if result else None


def get_parent_number(user_id):
    connection = sql.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("SELECT parent_number FROM Users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    connection.commit()
    return result[0] if result else None


def get_lesson(date, time, topic, age):
    connection = sql.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute('''
    SELECT * FROM Users WHERE date = ? AND time = ? AND topic = ? AND age = ?
    ''', (date, time, topic, age))
    result = cursor.fetchone()
    connection.commit()
    

#True - запись прошла успешно | False - нет места | None - уже записан
def sign_up_to_lesson(date : str, time : str, topic : str, age : str, student_id : str):
    connection = sql.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("SELECT child_name FROM Users WHERE user_id = ?", (student_id,))
    student_name = (cursor.fetchone())[0]

    cursor.execute('''
        SELECT * FROM Lessons WHERE date = ? AND time = ? AND topic = ? AND age = ?
    ''', (date, time, topic, age))
    lesson_row = cursor.fetchone()

    if lesson_row:
        cursor.execute("SELECT student FROM Lessons WHERE date = ? AND time = ? AND topic = ? AND age = ?", (date, time, topic, age))
        students = (cursor.fetchone())[0]
        students = ast.literal_eval(students)
        if student_name in students:
            return None
        if len(students)<8:
            students.append(student_name)
            cursor.execute('''
                UPDATE Lessons SET student = ? WHERE date = ? AND time = ? AND topic = ? AND age = ?
            ''', (str(students), date, time, topic, age))
            connection.commit()
            return True
        else:
            connection.commit()
            return False
    else:
        students = [student_name]
        cursor.execute('''
            INSERT INTO Lessons (date, time, topic, age, student) VALUES (?, ?, ?, ?, ?)
        ''', (date, time, topic, age, str(students)))

    connection.commit()
    return True


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
