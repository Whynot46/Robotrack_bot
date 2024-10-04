import sqlite3 as sql
import pandas as pd
import ast
from src.config import DB_PATH


def add_new_user(user_id : int, username : str, child_name : str, child_age : str, parent_number : str):
    connection = sql.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute('''
            INSERT INTO Users (user_id, username, child_name, child_birthday, parent_number)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, username, child_name, child_age, parent_number))
    connection.commit()
    connection.close()


def add_lesson(date : str, time : str, topic : str, age : str):
    connection = sql.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute('''
            INSERT INTO Users (date, time, topic, age)
            VALUES (?, ?, ?, ?)
        ''', (date, time, topic, age))
    connection.commit()
    connection.close()
    

def is_old(user_id : int) -> bool:
    connection = sql.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("SELECT 1 FROM Users WHERE user_id = ?", (user_id,))
    result  = cursor.fetchone()
    connection.commit()
    connection.close()

    return bool(result)


def is_admin(user_id : int) -> bool:
    for admin in get_admins_list():
        if user_id == admin[0]:
            return True
    
    return False


def get_username(user_id : int) -> str:
    connection = sql.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("SELECT username FROM Users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    connection.commit()
    connection.close()

    return result[0] if result else None


def get_child_name(user_id : int) -> str:
    connection = sql.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("SELECT child_name FROM Users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    connection.commit()
    connection.close()

    return result[0] if result else None


def get_child_birthday(user_id : int) -> str:
    connection = sql.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("SELECT child_birthday FROM Users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    connection.commit()
    connection.close()

    return result[0] if result else None


def get_parent_number(user_id : int) -> str:
    connection = sql.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("SELECT parent_number FROM Users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    connection.commit()
    connection.close()
    
    return result[0] if result else None


def get_user_lessons(user_id: int) -> list:
    child_name = get_child_name(user_id)
    connection = sql.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Lessons")
    lessons = cursor.fetchall()

    if len(lessons)>0:
        user_lessons = []
        for lesson in lessons:
            if child_name in lesson[4]:
                user_lessons.append(lesson)

        connection.close()

        return user_lessons
    
    else:
        return []


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
            connection.close()
            return None
        if len(students)<8:
            students.append(student_name)
            cursor.execute('''
                UPDATE Lessons SET student = ? WHERE date = ? AND time = ? AND topic = ? AND age = ?
            ''', (str(students), date, time, topic, age))
            connection.commit()
            connection.close()
            return True
        else:
            connection.commit()
            connection.close()
            return False
    else:
        students = [student_name]
        cursor.execute('''
            INSERT INTO Lessons (date, time, topic, age, student) VALUES (?, ?, ?, ?, ?)
        ''', (date, time, topic, age, str(students)))

    connection.commit()
    connection.close()

    return True


def get_users_data():
    connection = sql.connect(DB_PATH) 
    xlsx_file = pd.read_sql_query('SELECT user_id, username, child_name, child_birthday, parent_number FROM Users', connection) 
    xlsx_file.to_excel("./db/users_data.xlsx", index=False)  
    connection.close() 


def get_lessons_data():
    connection = sql.connect(DB_PATH) 
    xlsx_file = pd.read_sql_query('SELECT date, time, topic, age FROM Lessons', connection) 
    xlsx_file.to_excel("./db/lessons_data.xlsx", index=False)  
    connection.close() 


def get_shedule_data():
    connection = sql.connect(DB_PATH) 
    xlsx_file = pd.read_sql_query('SELECT weekday, lessons FROM Shedule', connection) 
    xlsx_file.to_excel("./db/shedule_data.xlsx", index=False)  
    connection.close() 


def get_lessons(weekday : str) -> list: # list of tuple
    connection = sql.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("SELECT lessons FROM Shedule WHERE weekday = ?", (weekday,))
    results = cursor.fetchall()
    connection.close()

    results = str(results[0])
    results = results[2:-3]
    lessons = ast.literal_eval(results)

    return lessons


def get_lesson_children(date : str, time : str, topic : str, age : str) -> list: # list of str (ФИО)
    connection = sql.connect(DB_PATH)
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT student FROM Lessons WHERE date = ? AND time = ? AND topic = ? AND age = ?", (date, time, topic, age))
        students = (cursor.fetchone())[0]
        connection.close()
        students = ast.literal_eval(students)
        return students
    except:
        return []


def delete_child_from_lesson(child : str,  date : str, time : str, topic : str, age : str) -> None:
    connection = sql.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("SELECT student FROM Lessons WHERE date = ? AND time = ? AND topic = ? AND age = ?", (date, time, topic, age))
    students = (cursor.fetchone())[0]
    students = ast.literal_eval(students)
    students.remove(child)
    cursor.execute("UPDATE Lessons SET student = ? WHERE date = ? AND time = ? AND topic = ? AND age = ?", (str(students), date, time, topic, age))
    connection.commit()
    connection.close()


def get_admins_list() -> list:  # list of tuples
    connection = sql.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Admins")
    admins = cursor.fetchall()
    connection.close()
    return admins
