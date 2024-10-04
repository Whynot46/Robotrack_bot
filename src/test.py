# import sqlite3 as sql
# import ast

# DB_PATH = "./db/Data.db"


# #True - запись прошла успешно False - нет места None - уже записан
# def sign_up_to_lesson(date : str, time : str, topic : str, age : str, student_id : str):
#     connection = sql.connect(DB_PATH)
#     cursor = connection.cursor()

#     cursor.execute("SELECT child_name FROM Users WHERE user_id = ?", (student_id,))
#     student_name = (cursor.fetchone())[0]

#     cursor.execute('''
#         SELECT * FROM Lessons WHERE date = ? AND time = ? AND topic = ? AND age = ?
#     ''', (date, time, topic, age))
#     lesson_row = cursor.fetchone()

#     if lesson_row:
#         cursor.execute("SELECT student FROM Lessons WHERE date = ? AND time = ? AND topic = ? AND age = ?", (date, time, topic, age))
#         students = (cursor.fetchone())[0]
#         students = ast.literal_eval(students)
#         if student_name in students:
#             return None
#         if len(students)<8:
#             students.append(student_name)
#             cursor.execute('''
#                 UPDATE Lessons SET student = ? WHERE date = ? AND time = ? AND topic = ? AND age = ?
#             ''', (str(students), date, time, topic, age))
#             connection.commit()
#             return True
#         else:
#             connection.commit()
#             return False
#     else:
#         students = [student_name]
#         cursor.execute('''
#             INSERT INTO Lessons (date, time, topic, age, student) VALUES (?, ?, ?, ?, ?)
#         ''', (date, time, topic, age, str(students)))

#     connection.commit()
#     return True


# print(sign_up_to_lesson("16.11.2024", "10:00-11:40", "Робототехника", "4-6 лет", "1071349364"))

# from datetime import datetime

# def calculate_age(birth_date : str) -> int:
#     birth_date = datetime.strptime(birth_date_str, "%d.%m.%Y")
#     today = datetime.today()
#     age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
#     return age

# birth_date_str = "28.11.2004"
# age = calculate_age(birth_date_str)
# print(f"Age: {age}")

text = "Робототехника 4-6 лет 16:20-18:00\nПятница 04.10.2024\n\nФамилия Имя Отчество"

lesson, children_str = text.split("\n\n", 1)
part_1, part_2 = lesson.split("\n")
topic_age, time = part_1.rsplit(" ", 1)
topic, age = topic_age.split(" ", 1)
weekday, date = part_2.split(" ", 1)
print(date, time, topic, age)