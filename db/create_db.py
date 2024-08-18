import sqlite3 as sql


connection = sql.connect('./db/User_data.db')
cursor = connection.cursor()

cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS Users (
        username TEXT NOT NULL,
        user_id INTEGER NOT NULL,
        )
        ''')

connection.commit()