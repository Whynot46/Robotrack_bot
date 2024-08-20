import sqlite3


connection = sqlite3.connect("./db/Data.db")
cursor = connection.cursor()

# Очищаем таблицу Users
cursor.execute('DELETE FROM Users')

connection.commit()
connection.close()