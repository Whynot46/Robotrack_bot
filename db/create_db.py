import sqlite3 as sql

connection = sql.connect('./db/Data.db')
cursor = connection.cursor()

cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        child_name TEXT NOT NULL,
        child_birthday INTEGER NOT NULL,
        parent_number TEXT NOT NULL
        )
        ''')

cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS Lessons (
        date TEXT NOT NULL,
        time TEXT NOT NULL,
        topic TEXT NOT NULL,
        age TEXT NOT NULL,
        student TEXT
        )
        ''')

cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS Shedule (
        weekday TEXT NOT NULL,
        lessons TEXT NOT NULL
        )
        ''')

cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS Admins (
        id INTEGER NOT NULL,
        username TEXT NOT NULL
        )
        ''')

connection.commit()
connection.close()