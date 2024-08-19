import sqlite3 as sql


connection = sql.connect('./db/Data.db')
cursor = connection.cursor()


cursor.execute('''
        INSERT INTO Shedule (user_id, username, child_name, child_age, parent_number)
        VALUES (?, ?)
    ''', ("Понедельник", str([])))

cursor.execute('''
        INSERT INTO Shedule (user_id, username, child_name, child_age, parent_number)
        VALUES (?, ?)
    ''', ("Вторник", str([])))

cursor.execute('''
        INSERT INTO Shedule (user_id, username, child_name, child_age, parent_number)
        VALUES (?, ?)
    ''', ("Среда", str([])))

cursor.execute('''
        INSERT INTO Shedule (user_id, username, child_name, child_age, parent_number)
        VALUES (?, ?)
    ''', ("Четверг", str([])))

cursor.execute('''
        INSERT INTO Shedule (user_id, username, child_name, child_age, parent_number)
        VALUES (?, ?)
    ''', ("Пятница", str([])))

cursor.execute('''
        INSERT INTO Shedule (user_id, username, child_name, child_age, parent_number)
        VALUES (?, ?)
    ''', ("Суббота", str([])))

cursor.execute('''
        INSERT INTO Shedule (user_id, username, child_name, child_age, parent_number)
        VALUES (?, ?)
    ''', ("Воскресенье", str([])))


connection.commit()
connection.close()