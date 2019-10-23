import sqlite3


class LikePontos:
    def __init__(self, tabela, id_pontoturistico, id_usuario, data, avaliacao):
        self.tabela = tabela
        self.id_pontoturistico = id_pontoturistico
        self.id_usuario = id_usuario
        self.data = data
        self.avaliacao = avaliacao
    
    def save(self):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('''INSERT INTO {}(id_pontoturistico, id_usuario, data, avaliacao) VALUES(?, ?, ?, ?)'''.format(self.tabela), (self.id_pontoturistico, self.id_usuario, self.data, self.avaliacao))
        connection.commit()
        connection.close()

    def getall(self):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        cursor.execute('''SELECT * FROM {}'''.format(self.tabela))
        rows = cursor.fetchall()

        return rows
