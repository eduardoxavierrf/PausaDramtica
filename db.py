import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()
cursor.execute(
'''
CREATE TABLE IF NOT EXISTS usuarios(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    senha TEXT NOT NULL
)
'''
)