import sqlite3 as sql


connection = sql.connect('./db/Data.db')
cursor = connection.cursor()


cursor.execute('''
        INSERT INTO Shedule (weekday, lessons)
        VALUES (?, ?)
    ''', ("Понедельник", str([])))

cursor.execute('''
        INSERT INTO Shedule (weekday, lessons)
        VALUES (?, ?)
    ''', ("Вторник", str([
        ("Робототехника", "10-14 лет", "10:00-11:40"),
        ("Робототехника", "7-9 лет", "16:20-18:00"),
        ("3D моделирование", "10+ лет", "18:20-20:00")
    ])))

cursor.execute('''
        INSERT INTO Shedule (weekday, lessons)
        VALUES (?, ?)
    ''', ("Среда", str([
        ("Робототехника", "7-9 лет", "10:00-11:40"),
        ("Робототехника", "4-5 лет", "16:20-18:00"),
        ("Робототехника", "7-9 лет", "18:20-20:00", ),
    ])))

cursor.execute('''
        INSERT INTO Shedule (weekday, lessons)
        VALUES (?, ?)
    ''', ("Четверг", str([
        ("Робототехника", "10-14 лет", "10:00-11:40"),
        ("Робототехника", "7-8 лет", "16:20-18:00"),
        ("Робототехника", "4-6 лет", "18:20-20:00")
    ])))

cursor.execute('''
        INSERT INTO Shedule (weekday, lessons)
        VALUES (?, ?)
    ''', ("Пятница", str([
        ("Робототехника", "7-9 лет", "10:00-11:40"),
        ("Робототехника", "4-6 лет", "16:20-18:00"),
        ("Робототехника", "7-9 лет", "18:20-20:00")
    ])))

cursor.execute('''
        INSERT INTO Shedule (weekday, lessons)
        VALUES (?, ?)
    ''', ("Суббота", str([
        ("Робототехника", "4-6 лет", "10:00-11:40"),
        ("Робототехника", "7-9 лет", "12:00-13:40"),
        ("Робототехника", "10-14 лет", "14:20-16:00"),
        ("Трекдуино", "10-14 лет", "16:20-18:00"),
        ("Minecraft Python", "10+ лет", "18:20-20:00")
    ])))

cursor.execute('''
        INSERT INTO Shedule (weekday, lessons)
        VALUES (?, ?)
    ''', ("Воскресенье", str([
        ("Робототехника", "4-6 лет", "10:00-11:40"),
        ("Робототехника", "7-9 лет", "12:00-13:40"),
        ("Трекдуино", "10-14 лет", "14:20-16:00"),
        ("Python", "10+ лет", "16:20-18:00"),
        ("3D моделирование", "10+ лет", "18:20-20:00")
    ])))


connection.commit()
connection.close()