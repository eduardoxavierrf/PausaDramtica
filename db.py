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

cursor = connection.cursor()

cursor.execute(
'''
CREATE TABLE IF NOT EXISTS pontos_turisticos(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    imagem TEXT NOT NULL,
    descricao TEXT NOT NULL,
    lugar TEXT NOT NULL
)
'''
)

connection.commit()

connection.close()