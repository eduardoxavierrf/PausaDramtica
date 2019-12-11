import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()
cursor.execute(
'''
CREATE TABLE IF NOT EXISTS usuarios(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    senha TEXT NOT NULL,
    tipo TEXT NOT NULL
)
'''
)

cursor.execute(
'''
CREATE TABLE IF NOT EXISTS pontos_turisticos(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    descricao TEXT NOT NULL,
    lugar TEXT NOT NULL,
    imagem TEXT NOT NULL,
    like INTEGER,
    dislike INTEGER
)
'''
)

cursor.execute(
'''
CREATE TABLE IF NOT EXISTS passeios(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    guia TEXT NOT NULL,
    ponto TEXT NOT NULL,
    data TEXT NOT NULL
)
'''
)
cursor.execute(
'''
CREATE TABLE IF NOT EXISTS like(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    id_usuarios INTEGER NOT NULL,
    id_ponto INTEGER NOT NULL,
    likeOrDislike INTEGER NOT NULL,

    FOREIGN KEY (id_usuarios) REFERENCES usuarios(id),
    FOREIGN KEY (id_ponto) REFERENCES pontos_turisticos(id)
)
'''
)
cursor.execute(
'''
CREATE TABLE IF NOT EXISTS passeios1(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    id_passeio INTEGER NOT NULL,
    name_turista TEXT NOT NULL,
    

    FOREIGN KEY (id_passeio) REFERENCES passeios(id),
    FOREIGN KEY (name_turista) REFERENCES usuarios(username)
)
'''
)

connection.commit()

connection.close()