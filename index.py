from flask import Flask, render_template, request, redirect, url_for

from models.usuario import Usuario

import sqlite3

app = Flask(__name__)

connection = sqlite3.connect('database.db')

def pesquisar_pontos():
    global connection
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    pesquisa = str(input("Digite o lugar para ver seus pontos turísticos: "))
    lista = cursor.execute(
    '''
    SELECT name, descricao FROM pontos_turisticos WHERE lugar = ''' + "'" + pesquisa + "'"
    ).fetchall()
    connection.close()
    return lista

def criar_pontos():
    global connection
    connection = sqlite3.connect('database.db')
    name = str(input("Digite o nome do ponto turistico: "))
    descricao = str(input("Digite a descricao do ponto turistico: "))
    lugar = str(input("Digite o lugar do ponto turistico: "))
    cursor = connection.cursor()
    lista = cursor.execute(
    '''
    SELECT name FROM pontos_turisticos WHERE name = ''' + "'" + name + "'"
    ).fetchall()
    connection.close()
    if(lista == []):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        lista = cursor.execute(
        '''
        INSERT INTO pontos_turisticos(name, descricao, lugar)
        VALUES ('''+"'"+name+"', "+"'"+descricao+"', "+"'"+lugar+"');"
        )
        connection.commit()
        connection.close()
        print("Ponto criado")
    else:
        print("Ja existe")

cursor = connection.cursor()

cursor.execute(
'''
CREATE TABLE IF NOT EXISTS pontos_turisticos(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    descricao TEXT NOT NULL,
    lugar TEXT NOT NULL
)
'''
)

connection.commit()

connection.close()


@app.route('/')
def main():
    return redirect(url_for('index'))

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        senha = request.form['senha']

        user = Usuario(tabela='usuarios', username=username, senha=senha)
        validate = user.autenticar()

        if validate:
            return redirect(url_for('index'))
        else:
            return render_template('Login.html')
    if request.method == 'GET':
        return render_template('Login.html')


@app.route('/registrar', methods = ['POST', 'GET'])
def registrar():
    if request.method == 'POST':
        username = request.form['username']
        senha = request.form['senha']
        email = request.form['email']

        user = Usuario(tabela='usuarios', username=username, senha=senha, email=email)
        validate = user.registrar()

        if validate:
            return redirect(url_for('login'))
        else:
            return render_template('registro.html')
    if request.method == 'GET':
        return render_template('registro.html')


if __name__ == '__main__':
    app.run(debug=True)
